from odoo import models, fields, api


class DoctorSlot(models.Model):
    _name = 'doctor.slot'
    _description = 'Doctor Time Slot'

    # الاسم المعروض تلقائياً: دكتور + وقت البداية والنهاية
    name = fields.Char(string="Name", compute="_compute_name")

    # اختيار الدكتور لكل slot
    doctor_id = fields.Many2one(
        'clinic.doctor',  # رابط لموديل الدكتور (تم التغيير من hospital → clinic)
        string="Doctor",
        required=True
    )

    # تاريخ الموعد
    date = fields.Date(
        string="Date"
    )

    # زمن البداية
    start_time = fields.Float(
        string="Start Time",
        required=True
    )

    # زمن النهاية
    end_time = fields.Float(
        string="End Time",
        required=True
    )

    # حالة الموعد
    state = fields.Selection([
        ('available', 'Available'),
        ('booked', 'Booked')
    ],
        string="State",
        default='available'
    )

    # حساب الاسم تلقائياً
    @api.depends('doctor_id', 'start_time', 'end_time')
    def _compute_name(self):
        for rec in self:
            doctor = rec.doctor_id.name if rec.doctor_id else ""
            rec.name = f"{doctor} {rec.start_time} - {rec.end_time}"

    # دالة لحجز الموعد
    def action_book(self):
        for rec in self:
            rec.state = 'booked'