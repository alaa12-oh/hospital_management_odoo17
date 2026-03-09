from odoo import models, fields, api


class PatientVisit(models.Model):
    _name = 'patient.visit'
    _description = 'Patient Visit'

    # رقم الزيارة
    name = fields.Char(
        string="Visit Number",
        readonly=True,
        copy=False,
        default="New"
    )

    # المريض
    patient_id = fields.Many2one(
        'clinic.patient',
        string="Patient",
        required=True
    )

    # الطبيب
    doctor_id = fields.Many2one(
        'clinic.doctor',
        string="Doctor",
        required=True
    )

    # نوع الزيارة
    visit_type = fields.Selection([
        ('emergency', 'طوارئ'),
        ('review', 'مراجعة'),
        ('checkup', 'كشف'),
    ], string="Visit Type")

    # تاريخ الزيارة
    visit_date = fields.Date(
        string="Visit Date",
        default=fields.Date.today
    )

    # منشئ الزيارة
    visit_creater = fields.Many2one(
        'res.users',
        string="Created By",
        default=lambda self: self.env.user
    )

    # الشكوى الرئيسية
    chief_complaint = fields.Text(
        string="Chief Complaint"
    )

    # التشخيص
    diagnosis = fields.Text(
        string="Diagnosis"
    )

    # ملاحظات الطبيب
    note = fields.Text(
        string="Doctor Notes"
    )

    # حالة الزيارة
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_payment', 'Waiting Payment'),
        ('waiting_doctor', 'Waiting Doctor'),
        ('with_doctor', 'With Doctor'),
        ('done', 'Done')
    ], string="Status", default="draft")

    # توليد رقم الزيارة
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('patient.visit') or 'New'
        return super(PatientVisit, self).create(vals)