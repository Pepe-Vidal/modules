# -*- coding: utf-8 -*-

from odoo import models, fields, api


class student(models.Model):
    _name = 'school.student'
    _description = 'The students'

    name = fields.Char(string="Nombre",required=True)
    year = fields.Integer()
    topic_id = fields.Many2many("school.topic")


class topic(models.Model):
    _name = 'school.topic'
    _description = 'The topics'

    name = fields.Char(string="Topic name",required=True)
    students = fields.Many2many("school.student")

class course(models.Model):
    _name = 'school.course'
    _description = 'Course'

    name = fields.Char()
    topic = fields.Many2many("school.topic")
    students = fields.Many2many("school.student")
    repeaters = fields.Many2many(comodel_name='school.student', 
                            relation='course_students_repeaters_rel', 
                            column1='course_id', 
                            column2='student_id') 
    
    