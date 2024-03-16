from src.particles.particle_renderer import ParticleRenderer
from src.particles.insertion_sort import InsertionSort


class ParticleMaster:

    __particles = dict()

    def __init__(self, loader, projection_matrix: list[list]):
        self.__renderer = ParticleRenderer(loader, projection_matrix)

    def update(self, camera):
        try:
            for particles in self.__particles.values():
                for p in particles:
                    still_alive = p.update(camera)
                    if not still_alive:
                        particles.remove(p)
                        if not particles:
                            [self.__particles.pop(k) for k, v in self.__particles.items() if v is particles]
                InsertionSort.sort_high_to_low(particles)
        except RuntimeError:
            # the dictionary will change size but this is exactly what we want
            pass

    def render_particles(self, camera):
        self.__renderer.render(self.__particles, camera)

    def clean_up(self):
        self.__renderer.clean_up()

    @staticmethod
    def add_particle(particle):
        particle_list = ParticleMaster.__particles.get(particle.get_texture())
        if particle_list is None:
            particle_list = []
            ParticleMaster.__particles.update({particle.get_texture(): particle_list})
        particle_list.append(particle)
