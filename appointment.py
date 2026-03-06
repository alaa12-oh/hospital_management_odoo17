from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ClinicAppointment(models.Model):
    _name = 'clinic.appointment'
    _description = 'Clinic Appointment'

    patient_id = fields.Many2one(
        'clinic.patient',
        string="Patient",
        required=True
    )
    doctor_id = fields.Many2one(
        'clinic.doctor',
        string="Doctor",
        required=True
    )
    appointment_date = fields.Date(
        string="Appointment Date",
        required=True
    )
    slot_id = fields.Many2one(
        'clinic.doctor.slot',
        string="Doctor Slot",
        domain="[('doctor_id','=',doctor_id),('slot_date','=',appointment_date),('state','=','available')]",
        required=True
    )
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('cancel', 'Cancel')],
        string="Status",
        default='draft'
    )

    # Confirm action
    def action_confirm(self):
        for record in self:
            if record.slot_id.state != 'available':
                raise ValidationError("Selected slot is not available!")
            record.state = 'confirmed'
            record.slot_id.state = 'booked'

    # Cancel action
    def action_cancel(self):
        for record in self:
            record.state = 'cancel'
            record.slot_id.state = 'available'  # تعيد الفتحة متاحة