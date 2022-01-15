from pygame.sprite import Group


class ModifiedGroup(Group):
    def draw(self, surface):
        """draw all sprites onto the surface
        Group.draw(surface): return Rect_list
        Draws all of the member sprites onto the given surface.
        """
        sprites = self.sprites()
        if hasattr(surface, "blits"):
            self.spritedict.update(
                # draw_rect - атрибут у объектов класса sprite и других наследуемых,
                # нужен для удобства при различении rect при отрисовке и при обработке столкновений
                zip(sprites, surface.blits((spr.image, spr.draw_rect) for spr in sprites))
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(spr.image, spr.draw_rect)
        self.lostsprites = []
        dirty = self.lostsprites

        return dirty
