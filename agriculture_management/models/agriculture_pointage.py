# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AgriculturePointage(models.Model):
    _name = 'agriculture.pointage'
    _rec_name = 'name'

    name = fields.Char(string="Nom", compute='_compute_name', recursive=True, store=True)
    date = fields.Date(string="Date", required=True, )
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    user_id = fields.Many2one(comodel_name="res.users", string="Opérateur", required=True, default=lambda self: self.env.user)
    secteur = fields.Selection(string="Secteur", selection=[('secteur_1', 'Secteur 1'),
                                                            ('secteur_2', 'Secteur 2'),
                                                            ('secteur_3', 'Secteur 3'),
                                                            ('secteur_4', 'Secteur 4'),
                                                            ('secteur_5', 'Secteur 5'),
                                                            ('secteur_6', 'Secteur 6'),], required=True, )
    eau_start = fields.Datetime(string="Début arossage", required=False, )
    eau_end = fields.Datetime(string="Fin arossage", required=False, )
    eau_quantity = fields.Float(string="Quantité d'eau (L)",  required=False, compute="compute_water_quantity")
    azote = fields.Float(string="Azote (kg)",  required=False, )
    phosphore = fields.Float(string="Phosphore (kg)",  required=False, )
    engrais = fields.Float(string="Engrais (kg)",  required=False, )
    potassium = fields.Float(string="Potassium(kg)",  required=False, )
    ammonium_nitrate = fields.Float(string="Ammonitrate (kg)", required=False, )
    soufre = fields.Float(string="Soufre (kg)", required=False, )

    @api.depends('secteur', 'date')
    def _compute_name(self):
        for rec in self:
            rec.name = f"Suivi du {dict(self._fields['secteur'].selection).get(rec.secteur)} le {rec.date}"

    # @api.depends('secteur', 'date')
    def compute_water_quantity(self):
        for rec in self:
            tot_sec = (rec.eau_end - rec.eau_start).total_seconds()
            rec.eau_quantity = tot_sec * 5