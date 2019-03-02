import environment.builder as builder
import config
import math

class BoosterAgent:
    def __init__(self, world, W, H, np_random):
        self.body = builder.generate_booster(world, W, H, np_random)
        self.np_random = np_random
        self.MAIN_ENGINE_POWER = config.MAIN_ENGINE_POWER * 1/config.FPS
        self.SIDE_ENGINE_POWER = config.SIDE_ENGINE_POWER * 1/config.FPS

    # Actions
    def fireMainEngine(self, m_power, alpha, create_particle, record_metrics):

        dispersion = self.np_random.uniform(-0.1, +0.1)
        impulse_pos = (self.body.position[0], self.body.position[1])

        if self.MAIN_ENGINE_POWER:
            p = create_particle(3.5, impulse_pos[0], impulse_pos[1], m_power)  # particles are just a decoration, 3.5 is here to make particle speed adequate
            p.coldGas = False  

            angle = -(self.body.angle +alpha + dispersion)
            Ft = self.MAIN_ENGINE_POWER * m_power 
            Fy = Ft*math.cos(angle)
            Fx = Ft*math.sin(angle)

            record_metrics({"Fx":Fx, "Fy":Fy, "Ft":math.sqrt(Fx*Fx + Fy*Fy)})

            p.ApplyLinearImpulse((-Fx, -Fy), impulse_pos,True)
            self.body.ApplyLinearImpulse((Fx, Fy),
                                            impulse_pos, True)


    def fireSideEngine(self, s_power, direction, create_particle):

        dispersion = self.np_random.uniform(-0.1, +0.1)
        impulse_pos = (self.body.position[0] 
                            - config.SIDE_ENGINE_HEIGHT*math.sin(self.body.angle)
                            + direction*(config.SIDE_ENGINE_AWAY/2)*math.cos(self.body.angle), 
                       self.body.position[1] 
                            + config.SIDE_ENGINE_HEIGHT*math.cos(self.body.angle)
                            + direction*(config.SIDE_ENGINE_AWAY/2)*math.sin(self.body.angle))

        if self.SIDE_ENGINE_POWER:
            p = create_particle(0.7, impulse_pos[0], impulse_pos[1], s_power)
            p.coldGas = True

            angle = self.body.angle + dispersion 
            Fs = direction*self.SIDE_ENGINE_POWER * s_power
            Fx = Fs*math.cos(angle)
            Fy = Fs*math.sin(angle)

            p.ApplyLinearImpulse((Fx, Fy), impulse_pos, True)
            self.body.ApplyLinearImpulse((-Fx, -Fy), impulse_pos, True)





