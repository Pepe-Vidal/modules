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
    
class tramos(models.Model):
    _name = 'wheel_speed.tramos'
    _description = 'tramos de las carreras'
    
    name = fields.Char()
    distancia = fields.Float()
    grados = fields.Float()
    
    
    
    
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
    
    tramos = fields.Many2many('wheel_speed.tramos')

    distancia = fields.Float()
    time1 = fields.Float()
    time2 = fields.Float()
    winner = fields.Char()
    
    
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
            
    def simulate_race(self):         
      for c in self:
        player1 = c.player1
        player2 = c.player2
        car1 = c.car1
        car2 = c.car2
        
        vel_ini_car1 = 0
        vel_ini_car2 = 0
        
        time_car1 = 0
        time_car2 = 0
        
        tramos_carera = c.tramos
        
        for t in tramos_carera:
            
            if t.grados == 0:

                if (vel_ini_car1 == 0 ):
                    time_vel_max_car1 = ((car1.max_vel * car1.aceleracion)/100) * (car1.max_vel/100)
                else:
                    time_vel_max_car1 = ((car1.max_vel * car1.aceleracion)/100) * (car1.max_vel/100) - ((vel_ini_car1 * car1.aceleracion)/100) * (car1.max_vel/100)

                distancia_vel_max_car1 = ((car1.max_vel/2) * (5/18)) * time_vel_max_car1

                if (distancia_vel_max_car1 < c.distancia ):
                    time_car1 += ((t.distancia - distancia_vel_max_car1)/(car1.max_vel * (5/18)) ) + time_vel_max_car1
                else:
                    time_car1 += (t.distancia * time_vel_max_car1) / distancia_vel_max_car1
                
                
                if (vel_ini_car2 == 0 ):
                    time_vel_max_car2 = ((car2.max_vel * car2.aceleracion)/100) * (car2.max_vel/100)
                else:
                    time_vel_max_car2 = ((car2.max_vel * car2.aceleracion)/100) * (car2.max_vel/100)- ((vel_ini_car2 * car2.aceleracion)/100) * (car2.max_vel/100)
                  
                distancia_vel_max_car2 = ((car2.max_vel/2) * (5/18)) * time_vel_max_car2
                
                if (distancia_vel_max_car2 < c.distancia ):
                    time_car2 += ((t.distancia - distancia_vel_max_car2)/(car2.max_vel * (5/18))) + time_vel_max_car2
                else:
                    time_car2 += (t.distancia * time_vel_max_car2) / distancia_vel_max_car2
                 
            else:

                #CALCULAR TIEMPO COCHE 1 CURVA
                velocidad_max_curva = t.distancia / ((t.grados * 100 / 360) /10)

                velocidad_curva_car1 = velocidad_max_curva + car1.agarre - (car1.coef_aer*150)

                if velocidad_curva_car1 > car1.max_vel:
                    velocidad_curva_car1 = car1.max_vel * (car1.freno /100)
                else:
                    velocidad_curva_car1 = velocidad_curva_car1 * (car1.freno /100)

                
                vel_ini_car1 = velocidad_curva_car1
                time_car1 += (t.distancia/(velocidad_curva_car1 * (5/18)))
                
                #CALCULAR TIEMPO COCHE 1 CURVA
                velocidad_curva_car2 = velocidad_max_curva + car2.agarre -(car2.coef_aer*150)

                if velocidad_curva_car2 > car2.max_vel:
                    velocidad_curva_car2 = car2.max_vel * (car2.freno /100)
                else:
                    velocidad_curva_car2 = velocidad_curva_car2 * (car2.freno /100)

                vel_ini_car2 = velocidad_curva_car2
                time_car2 += (t.distancia/(velocidad_curva_car2 * (5/18)))
             
        c.time1 = time_car1
        c.time2 = time_car2
        if (time_car2 > time_car1 ):
            c.winner = "car1"
        else:
            c.winner = "car2"
                          
                
                
    

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
    agarre = fields.Float(compute="_set_agarre")
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
          
    @api.depends('ruedas')
    def _set_agarre(self):          
      for rl in self:
          rl.agarre = rl.ruedas.agarre
          
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
    agarre = fields.Float(compute="_set_agarre")
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
          
    @api.depends('ruedas')
    def _set_agarre(self):          
      for rl in self:
          rl.agarre = rl.ruedas.agarre
          
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
    durabilidad = fields.Float(default = 100,readonly=True)
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
    durabilidad = fields.Float(default = 100,readonly=True)
    diametro = fields.Float()
    agarre = fields.Float()
    velocidad = fields.Float()
    
    @api.constrains('agarre')
    def comprobar_agarre(self):
        for w in self:
            if w.agarre > 200 or w.agarre < 0:
                raise ValidationError("El agarre tiene que ser entr 0 y 200.")


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
    durabilidad = fields.Float(default = 100,readonly=True)
    fuerza = fields.Float()
    
    @api.constrains('fuerza')
    def comprobar_agarre(self):
        for b in self:
            if b.fuerza > 200 or b.fuerza < 0:
                raise ValidationError("La furza tiene que ser entr 0 y 100.")
    
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
    durabilidad = fields.Float(default = 100,readonly=True)
    
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
    durabilidad = fields.Float(default = 100,readonly=True)
    velocidad = fields.Float()




