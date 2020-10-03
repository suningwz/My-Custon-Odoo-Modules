# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
import re

from binascii import Error as binascii_error
from collections import defaultdict
from operator import itemgetter
from odoo.http import request

from odoo import _, api, fields, models, modules, tools
from odoo.exceptions import UserError, AccessError
from odoo.osv import expression
from odoo.tools import groupby

_logger = logging.getLogger(__name__)
_image_dataurl = re.compile(r'(data:image/[a-z]+?);base64,([a-z0-9+/\n]{3,}=*)\n*([\'"])(?: data-filename="([^"]*)")?',
                            re.I)


class Project(models.Model):
    _inherit = 'project.project'

    @api.model
    def create(self, vals):
        # Prevent double project creation
        self = self.with_context(mail_create_nosubscribe=True)
        project = super(Project, self).create(vals)
        if not vals.get('subtask_project_id'):
            project.subtask_project_id = project.id
        if project.privacy_visibility == 'portal' and project.partner_id:
            project.message_subscribe(project.partner_id.ids)

        ######################################################
        print(vals)
        self.env['mail.message'].create({'message_type': "notification",
                                         "subtype_id": self.env.ref("mail.mt_note").id,
                                         'subject': f"New: {vals['name']}",
                                         'body': f"{project.user_id.name} Created this project",
                                         'model': 'project.project',
                                         'res_id': project.id,
                                         })
        #######################################################

        return project

    def write(self, vals):
        # directly compute is_favorite to dodge allow write access right
        if 'is_favorite' in vals:
            vals.pop('is_favorite')
            self._fields['is_favorite'].determine_inverse(self)
        res = super(Project, self).write(vals) if vals else True
        if 'active' in vals:
            # archiving/unarchiving a project does it on its tasks, too
            self.with_context(active_test=False).mapped('tasks').write({'active': vals['active']})
        if vals.get('partner_id') or vals.get('privacy_visibility'):
            for project in self.filtered(lambda project: project.privacy_visibility == 'portal'):
                project.message_subscribe(project.partner_id.ids)
        print(self)
        ######################################################
        self.env['mail.message'].create({'message_type': "notification",
                                         "subtype_id": self.env.ref("mail.mt_note").id,
                                         'subject': f"Edited: {self.name}",
                                         'body': f"{self.user_id.name} Edited this project",
                                         'model': 'project.project',
                                         'res_id': self.id,
                                         })
        #######################################################
        return res


class Task(models.Model):
    _inherit = 'project.task'

    @api.model
    def create(self, vals):
        # context: no_log, because subtype already handle this
        context = dict(self.env.context)
        # for default stage
        if vals.get('project_id') and not context.get('default_project_id'):
            context['default_project_id'] = vals.get('project_id')
        # user_id change: update date_assign
        if vals.get('user_id'):
            vals['date_assign'] = fields.Datetime.now()
        # Stage change: Update date_end if folded stage and date_last_stage_update
        if vals.get('stage_id'):
            vals.update(self.update_date_end(vals['stage_id']))
            vals['date_last_stage_update'] = fields.Datetime.now()
        # substask default values
        if vals.get('parent_id'):
            for fname, value in self._subtask_values_from_parent(vals['parent_id']).items():
                if fname not in vals:
                    vals[fname] = value
        task = super(Task, self.with_context(context)).create(vals)

        ######################################################
        self.env['mail.message'].create({'message_type': "notification",
                                         "subtype_id": self.env.ref("mail.mt_note").id,
                                         'subject': f"New: {task.name}",
                                         'body': f"This Task Created under '{task.project_id.name}' Project and is Assigned to {task.user_id.name}",
                                         'model': 'project.task',
                                         'res_id': task.id,
                                         })
        #######################################################
        return task

    def write(self, vals):
        now = fields.Datetime.now()
        # stage change: update date_last_stage_update
        if 'stage_id' in vals:
            vals.update(self.update_date_end(vals['stage_id']))
            vals['date_last_stage_update'] = now
            # reset kanban state when changing stage
            if 'kanban_state' not in vals:
                vals['kanban_state'] = 'normal'
        # user_id change: update date_assign
        if vals.get('user_id') and 'date_assign' not in vals:
            vals['date_assign'] = now

        result = super(Task, self).write(vals)
        # rating on stage
        if 'stage_id' in vals and vals.get('stage_id'):
            self.filtered(lambda x: x.project_id.rating_status == 'stage')._send_task_rating_mail(force_send=True)

        ######################################################
        self.env['mail.message'].create({'message_type': "notification",
                                         "subtype_id": self.env.ref("mail.mt_note").id,
                                         'subject': f"Edited: {self.name}",
                                         'body': f"This Task under '{self.project_id.name}' project and assigned to {self.user_id.name}  has been Edited",
                                         'model': 'project.task',
                                         'res_id': self.id,
                                         })
        #######################################################
        return result


class Message(models.Model):
    _inherit = 'mail.message'

    @api.model_create_multi
    def create(self, values_list):
        tracking_values_list = []
        for values in values_list:
            if 'email_from' not in values:  # needed to compute reply_to
                values['email_from'] = self._get_default_from()
            if not values.get('message_id'):
                values['message_id'] = self._get_message_id(values)
            if 'reply_to' not in values:
                values['reply_to'] = self._get_reply_to(values)
            if 'record_name' not in values and 'default_record_name' not in self.env.context:
                values['record_name'] = self._get_record_name(values)

            if 'attachment_ids' not in values:
                values['attachment_ids'] = []
            # extract base64 images
            if 'body' in values:
                Attachments = self.env['ir.attachment']
                data_to_url = {}

                def base64_to_boundary(match):
                    key = match.group(2)
                    if not data_to_url.get(key):
                        name = match.group(4) if match.group(4) else 'image%s' % len(data_to_url)
                        try:
                            attachment = Attachments.create({
                                'name': name,
                                'datas': match.group(2),
                                'res_model': values.get('model'),
                                'res_id': values.get('res_id'),
                            })
                        except binascii_error:
                            _logger.warning(
                                "Impossible to create an attachment out of badly formated base64 embedded image. Image has been removed.")
                            return match.group(
                                3)  # group(3) is the url ending single/double quote matched by the regexp
                        else:
                            attachment.generate_access_token()
                            values['attachment_ids'].append((4, attachment.id))
                            data_to_url[key] = [
                                '/web/image/%s?access_token=%s' % (attachment.id, attachment.access_token), name]
                    return '%s%s alt="%s"' % (data_to_url[key][0], match.group(3), data_to_url[key][1])

                values['body'] = _image_dataurl.sub(base64_to_boundary, tools.ustr(values['body']))

            # delegate creation of tracking after the create as sudo to avoid access rights issues
            tracking_values_list.append(values.pop('tracking_value_ids', False))

        messages = super(Message, self).create(values_list)

        check_attachment_access = []
        if all(isinstance(command, int) or command[0] in (4, 6) for values in values_list for command in
               values.get('attachment_ids')):
            for values in values_list:
                for command in values.get('attachment_ids'):
                    if isinstance(command, int):
                        check_attachment_access += [command]
                    elif command[0] == 6:
                        check_attachment_access += command[2]
                    else:  # command[0] == 4:
                        check_attachment_access += [command[1]]
        else:
            check_attachment_access = messages.mapped('attachment_ids').ids  # fallback on read if any unknow command
        if check_attachment_access:
            self.env['ir.attachment'].browse(check_attachment_access).check(mode='read')

        for message, values, tracking_values_cmd in zip(messages, values_list, tracking_values_list):
            if tracking_values_cmd:
                vals_lst = [dict(cmd[2], mail_message_id=message.id) for cmd in tracking_values_cmd if
                            len(cmd) == 3 and cmd[0] == 0]
                other_cmd = [cmd for cmd in tracking_values_cmd if len(cmd) != 3 or cmd[0] != 0]
                if vals_lst:
                    self.env['mail.tracking.value'].sudo().create(vals_lst)
                if other_cmd:
                    message.sudo().write({'tracking_value_ids': tracking_values_cmd})

            if message.is_thread_message(values):
                message._invalidate_documents(values.get('model'), values.get('res_id'))

        ######################################################
        if messages.message_type == 'comment' and messages.author_id.name != self.env.user.name:
            self.env['mail.message'].create({'message_type': "notification",
                                             "subtype_id": self.env.ref("mail.mt_note").id,
                                             'subject': f"New Message: from {messages.author_id.name}",
                                             'body': f"Check inbox for the channel/Person #{messages.record_name}",
                                             'model': messages.model,
                                             'res_id': messages.res_id,
                                             })
        #######################################################

        return messages