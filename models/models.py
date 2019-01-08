# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning
from dateutil.relativedelta import relativedelta

class gym(models.Model):
    _inherit = 'res.partner'

    uid = fields.Char('ID', readonly=1, default='New')
    plan = fields.Selection((('trial', 'Trial'), ('monthly', 'Monthly'), ('3-months', '3-Months'),
                             ('6-months', '6-Months'), ('yearly', 'Yearly')), 'Plan')
    price = fields.Integer('Quoted Price', readonly=False, compute="_calculate_amount")
    due = fields.Boolean(string='Due', readonly=1)
    dob = fields.Date(string='Date of birth', readonly=1, )
    due_amount = fields.Integer(string='Due Amount', readonly=1)
    paid_amount = fields.Integer(string='Amount Paid')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date', readonly=1)
    total_due = fields.Integer('Total due')
    # phone = fields.Integer('Phone number', required=1)

    @api.model
    def create(self, vals):
        if vals.get('uid', 'New') == 'New':
            vals['uid'] = self.env['ir.sequence'].next_by_code('pf.sequence') or 'New'

        result = super().create(vals)
        return result

    @api.depends('plan')
    def _calculate_amount(self):
        if self.plan:
            if self.plan == 'trial':
                self.price = 0
            elif self.plan == 'monthly':
                self.price = 1500
            elif self.plan == '3-months':
                self.price = 3600
            elif self.plan == '6-months':
                self.price = 6000
            elif self.plan == 'yearly':
                self.price = 8000

    @api.onchange('paid_amount')
    def _due_check(self):
        for rec in self:
            d_c = rec.price - rec.paid_amount
            if d_c > 0:
                rec.due_amount = d_c
                rec.due = True
            elif d_c == 0:
                rec.due_amount = 0
                rec.due = False

    @api.onchange('start_date')
    def _cal_end(self):
        if self.start_date:
            if self.plan == 'trial':
                dt = fields.Datetime.from_string(self.start_date) + relativedelta(days=3)
                self.end_date = fields.Datetime.to_string(dt)
            elif self.plan == 'monthly':
                dt = fields.Datetime.from_string(self.start_date) + relativedelta(months=1)
                self.end_date = fields.Datetime.to_string(dt)
            elif self.plan == '3-months':
                dt = fields.Datetime.from_string(self.start_date) + relativedelta(months=3)
                self.end_date = fields.Datetime.to_string(dt)
            elif self.plan == '6-months':
                dt = fields.Datetime.from_string(self.start_date) + relativedelta(months=6)
                self.end_date = fields.Datetime.to_string(dt)
            elif self.plan == 'yearly':
                date_start_dt = fields.Datetime.from_string(self.start_date)
                dt = date_start_dt + relativedelta(years=1)
                self.end_date = fields.Datetime.to_string(dt)
            elif not self.plan:
                raise Warning('Enter a plan to get the end date.')