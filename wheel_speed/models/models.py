 # -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
import string
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import math

class player(models.Model):
    _name = 'wheel_speed.player'
    _description = 'Players'

    name = fields.Char(required=True)
    passwd = fields.Char()
    avatar = fields.Image(max_width = 200 ,max_height = 200 )
    money = fields.Float()
    
    cars = fields.One2many('wheel_speed.car','player')
    
    
    available_cars = fields.Many2many('wheel_speed.car_type',compute="_get_available_cars")
    
    
    required_money_garaje = fields.Float(compute='_get_required_money_garaje')
    garaje_level = fields.Integer(default=1)
    
    def _get_required_money_garaje(self):
        for p in self:
            p.required_money_garaje = (p.garaje_level ** 1.274) * 964

            
    
    def update_garaje(self):  # ORM
        for p in self:
            required_money = p.required_money_garaje  # Smartbutton
            available_money = p.money
            if (required_money <= available_money):
                p.garaje_level += 1
                p.money = p.money - required_money
               
    def _get_available_cars(self):  # ORM
        for p in self:
            p.available_cars = self.env['wheel_speed.car_type'].search([])
    

class race(models.Model):
    _name = 'wheel_speed.race'
    _description = 'Race'
    
    name = fields.Char()
    date_start = fields.Datetime(readonly=True, default=fields.Datetime.now)
    date_end = fields.Datetime(compute='_get_time')
    
    player1 = fields.Many2one('wheel_speed.player')
    player2 = fields.Many2one('wheel_speed.player')
    car1 = fields.Many2one('wheel_speed.car')
    car2 = fields.Many2one('wheel_speed.car')
    
    
    @api.onchange('player1')
    def onchange_player1(self):
        return {
            'domain': {
                'car1': [('id', 'in', self.player1.cars.ids)],
                'player2': [('id', '!=', self.player1.id)],
            }
        }

    @api.onchange('player2')
    def onchange_player2(self):
        return {
            'domain': {
                'car2': [('id', 'in', self.player2.cars.ids)],
                'player1': [('id', '!=', self.player2.id)],
            }
        }
        
    @api.depends('date_start')
    def _get_time(self):
        for r in self:
            r.date_end = fields.Datetime.to_string(
                    fields.Datetime.from_string(r.date_start) + timedelta(minutes=60))            
    

class car(models.Model):
    _name = 'wheel_speed.car'
    _description = 'Cars'
    
    player = fields.Many2one('wheel_speed.player')
    type = fields.Many2one('wheel_speed.car_type', ondelete="restrict",required=True)

    name = fields.Char(related='type.name')
    marca = fields.Char(related='type.marca')
    modelo = fields.Char(related='type.modelo')
    foto = fields.Image(related='type.foto')
    motor = fields.Many2one('wheel_speed.engine')
    ruedas = fields.Many2one('wheel_speed.wheel')
    frenos = fields.Many2one('wheel_speed.brake')
    chasis = fields.Many2one('wheel_speed.chassis')
    suspension = fields.Many2one('wheel_speed.suspension')
    cv = fields.Float(compute="_set_cv")
    max_vel = fields.Float(compute="_set_vel_max")
    weight = fields.Float(related='type.weight')
    weight_total = fields.Float(compute="_set_weight")
    coef_aer = fields.Float(related='type.coef_aer')
    aceleracion = fields.Float(related='type.aceleracion')
    freno = fields.Float(compute="_set_freno")
    
    price_car = fields.Float(related='type.price_car')
    
    @api.onchange('type')
    def _onchange_piezas(self):
        self.motor = self.type.motor
        self.ruedas = self.type.ruedas
        self.frenos = self.type.frenos
        self.chasis = self.type.chasis
        self.suspension = self.type.suspension
        self.cv = self.type.cv
        self.max_vel = self.type.max_vel
        
    @api.depends('ruedas','motor','ruedas','suspension','weight_total','coef_aer')
    def _set_vel_max(self):          
      for r in self:
          max_vel = r.motor.velocidad + r.ruedas.velocidad + r.suspension.velocidad - (r.weight_total/100)
          r.max_vel = max_vel + (max_vel-(max_vel * r.coef_aer))/5
          
    @api.depends('ruedas','motor','chasis','frenos','ruedas','suspension','weight')
    def _set_weight(self):          
      for r in self:
          r.weight_total = r.weight + r.motor.peso + r.ruedas.peso + r.chasis.peso + r.frenos.peso + r.suspension.peso
          
    @api.depends('motor')
    def _set_cv(self):          
      for rl in self:
          rl.cv = rl.motor.cv
          
    @api.depends('frenos')
    def _set_freno(self):          
      for rl in self:
          rl.freno = rl.frenos.fuerza
    


class car_type(models.Model):
    _name = 'wheel_speed.car_type'
    _description = 'Cars Types'

    name = fields.Char(required=True)
    marca = fields.Char(required=True)
    modelo = fields.Char(required=True)
    foto = fields.Image(max_width = 200 ,max_height = 200 )
    motor = fields.Many2one('wheel_speed.engine')
    ruedas = fields.Many2one('wheel_speed.wheel')
    frenos = fields.Many2one('wheel_speed.brake')
    chasis = fields.Many2one('wheel_speed.chassis')
    suspension = fields.Many2one('wheel_speed.suspension')
    cv = fields.Float(compute="_set_cv")
    max_vel = fields.Float(compute="_set_vel_max")
    weight = fields.Float()
    weight_total = fields.Float(compute="_set_weight")
    coef_aer = fields.Float()
    aceleracion = fields.Float()
    freno = fields.Float(compute="_set_freno")
    
    price_car = fields.Float()
    
    
    @api.depends('ruedas','motor','ruedas','suspension','weight_total','coef_aer')
    def _set_vel_max(self):          
      for r in self:
          max_vel = r.motor.velocidad + r.ruedas.velocidad + r.suspension.velocidad - (r.weight_total/100)
          r.max_vel = max_vel + (max_vel-(max_vel * r.coef_aer))/5
          
    @api.depends('ruedas','motor','chasis','frenos','ruedas','suspension','weight')
    def _set_weight(self):          
      for r in self:
          r.weight_total = r.weight + r.motor.peso + r.ruedas.peso + r.chasis.peso + r.frenos.peso + r.suspension.peso
          
    @api.depends('motor')
    def _set_cv(self):          
      for rl in self:
          rl.cv = rl.motor.cv
          
    @api.depends('frenos')
    def _set_freno(self):          
      for rl in self:
          rl.freno = rl.frenos.fuerza
          

    def comprar(self):          
      for c in self:
        player = self.env['wheel_speed.player'].browse(self.env.context['ctx_car_type'])
        qty_cars = len(player.cars)
        required_money = c.price_car  # Smartbutton
        available_money = player.money
        if (required_money <= available_money and player.garaje_level > qty_cars ):
            player.money = player.money - required_money      
            self.env['wheel_speed.car'].create({
                "player": player.id,
                "type": c.id,
                "motor": c.motor.id,
                "ruedas": c.ruedas.id,
                "frenos": c.frenos.id,
                "chasis": c.chasis.id,
                "suspension": c.suspension.id
            })
   
    
class engine(models.Model):
    _name = 'wheel_speed.engine'
    _description = 'Motor'

    type = fields.Many2one('wheel_speed.engine_type', ondelete="restrict",required=True)
    
    name = fields.Char(related='type.name')
    foto = fields.Image(related='type.foto')
    peso = fields.Float(related='type.peso')
    durabilidad = fields.Float(related='type.durabilidad')
    cc = fields.Float(related='type.cc')
    cv = fields.Float(related='type.cv')
    velocidad = fields.Float(related='type.velocidad')
    
class engine_type(models.Model):
    _name = 'wheel_speed.engine_type'

    name = fields.Char(required=True)
    foto = fields.Image(max_width = 200 ,max_height = 200 )
    peso = fields.Float()
    durabilidad = fields.Float()
    cc = fields.Float()
    cv = fields.Float()
    velocidad = fields.Float()

    
class wheel(models.Model):
    _name = 'wheel_speed.wheel'
    _description = 'Ruedas'
    
    type = fields.Many2one('wheel_speed.wheel_type', ondelete="restrict",required=True)

    name = fields.Char(related='type.name')
    foto = fields.Image(related='type.foto')
    peso = fields.Float(related='type.peso')
    durabilidad = fields.Float(related='type.durabilidad')
    diametro = fields.Float(related='type.diametro')
    agarre = fields.Float(related='type.agarre')
    velocidad = fields.Float(related='type.velocidad')

class wheel_type(models.Model):
    _name = 'wheel_speed.wheel_type'

    name = fields.Char(required=True)
    foto = fields.Image(max_width = 200 ,max_height = 200 )
    peso = fields.Float()
    durabilidad = fields.Float()
    diametro = fields.Float()
    agarre = fields.Float()
    velocidad = fields.Float()


class brake(models.Model):
    _name = 'wheel_speed.brake'
    _description = 'Frenos'
    
    type = fields.Many2one('wheel_speed.brake_type', ondelete="restrict",required=True)
    
    name = fields.Char(related='type.name')
    foto = fields.Image(related='type.foto')
    peso = fields.Float(related='type.peso')
    durabilidad = fields.Float(related='type.durabilidad')
    fuerza = fields.Float(related='type.fuerza')
    
class brake_type(models.Model):
    _name = 'wheel_speed.brake_type'

    name = fields.Char(required=True)
    foto = fields.Image(max_width = 200 ,max_height = 200 )
    peso = fields.Float()
    durabilidad = fields.Float()
    fuerza = fields.Float()
    
class chassis(models.Model):
    _name = 'wheel_speed.chassis'
    _description = 'Chasis'
    
    type = fields.Many2one('wheel_speed.chassis_type', ondelete="restrict",required=True)
    
    name = fields.Char(related='type.name')
    foto = fields.Image(related='type.foto' )
    peso = fields.Float(related='type.peso')
    durabilidad = fields.Float(related='type.durabilidad')
    
class chassis_type(models.Model):
    _name = 'wheel_speed.chassis_type'
    
    name = fields.Char(required=True)
    foto = fields.Image(max_width = 200 ,max_height = 200 )
    peso = fields.Float()
    durabilidad = fields.Float()
    
class suspension(models.Model):
    _name = 'wheel_speed.suspension'
    _description = 'Suspension'
    
    type = fields.Many2one('wheel_speed.suspension_type', ondelete="restrict",required=True)
    
    name = fields.Char(related='type.name')
    foto = fields.Image(related='type.foto')
    peso = fields.Float(related='type.peso')
    durabilidad = fields.Float(related='type.durabilidad')
    velocidad = fields.Float(related='type.velocidad')
    
class suspension_type(models.Model):
    _name = 'wheel_speed.suspension_type'
    
    name = fields.Char(required=True)
    foto = fields.Image(max_width = 200 ,max_height = 200 )
    peso = fields.Float()
    durabilidad = fields.Float()
    velocidad = fields.Float()




