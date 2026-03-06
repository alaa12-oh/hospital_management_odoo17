from odoo import models, fields, api

class DoctorSlot(models.Model):
    _name = '.doctor.slot'
    _description = 'Doctor Time Slot'

    name = fields.Char(string="Name", compute="_compute_name")
    doctor_id = fields.Many2one('clinic.doctor', string="Doctor", required=True)
    slot_date = fields.Date(string="Slot Date")  # تم تعديل الاسم من date → slot_date
    start_time = fields.Float(string="Start Time", required=True)
    end_time = fields.Float(string="End Time", required=True)
    state = fields.Selection([
        ('available', 'Available'),
        ('booked', 'Booked')
    ], string="State", default='available')

    @api.depends('doctor_id', 'start_time', 'end_time')
    def _compute_name(self):
        for rec in self:
            doctor = rec.doctor_id.name if rec.doctor_id else ""
            rec.name = f"{doctor} {rec.start_time} - {rec.end_time}"

    def action_book(self):
        for rec in self:
            rec.state = 'booked'