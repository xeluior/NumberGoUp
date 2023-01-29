module main
    fn main: instantiates and runs GameManager

module gamemanager
    class GameManager
        public  init(void)              -> GameManager
        public  run(void)               -> void
        private event_loop(scene.Scene) -> void

module scenes
    abstract class Scene
        public      init(void)                                          -> Scene
        abstract    draw(pygame.surface.Surface)                        -> void
        abstract    update(void)                                        -> void
        public      handle(pygame.event.Event)                          -> void
    class TitleScreen implements Scene
        public      init(str, pygame.font.Font, (int, int))             -> TitleScreen
        public      draw(pygame.surface.Surface)                        -> void
        public      update(void)                                        -> void
        public      handle(pygame.event.Event)                          -> void
    class Level implements Scene
        public      init(int)                                           -> Level
        public      *entity_at(util.Point)                              -> Entity
        public      draw(pygame.surface.Surface)                        -> void
        public      handle(pygame.event.Event)                          -> void
        public      update(void)                                        -> void

module sprite
    class TextSprite implements pygame.sprite.Sprite
        public      init(str, pygame.font.Font, str, str, (int, int))   -> TextSprite
        public      set_text(str)                                       -> void
        public      set_color(str)                                      -> void
        public      set_font(pygame.font.Font)                          -> void
        private     render(void)                                        -> void
    abstract class Entity
        public      init(str)                                           -> Entity
        public      draw(pygame.surface.Surface)                        -> void
        private     anchor_point(void)                                  -> (int, int)
        abstract    move(util.Point, scenes.Level)                      -> void
        abstract    take_damage(int)                                    -> void
    class Enemy implements Entity
        public      init(str)                                           -> Enemy
        public      move(util.Point, scenes.Level)                      -> void
        public      take_damage(int)                                    -> void
    class Player implements Entity
        public      init(void)                                          -> Player
        public      *handle(pygame.event.Event)                         -> void
        public      *move(util.Direction)                               -> void
        public      take_damage(int)                                    -> void

new module scene
    abstract class Scene /* Component Class */
        public add(Scene) /* adds scene to the child list */
        public remove(Scene) /* removes the scene from the child list */
        public parent(void) /* returns the parent scene of the scene */
        public child(int) /* returns the nth child */
        public draw(pygame.surface.Surface) /* draws the scene onto the surface */
        public update(int) /* updates the scene given the number of milliseconds passed */
        public handle(pygame.event.Event) /* handles the event */
    class Level : Scene /* Composite class */
        public handle(event) /* reimplemented to only 
        
        