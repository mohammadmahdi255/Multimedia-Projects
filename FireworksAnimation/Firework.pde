import processing.sound.*;
import java.util.Iterator;

class Firework {
    ArrayList<Particle> particles = new ArrayList<>();
    Particle particle;
    
    PVector pos, v;
    
    int n_particles;
    boolean exploded = false;
    
    color hsb;
    float margin;
    
    SoundFile startSound;
    SoundFile endSound;
  

    Firework(int n_particles, float margin, int h, SoundFile startSound) {
        this(random(margin, width - margin), height, n_particles, margin, h, startSound);
    }
    
    Firework(float x, float y, int n_particles, float margin, int h, SoundFile startSound) {  
    this(
        new PVector(x, y),
        new PVector(random(-50, 50)/10, random(-250, -100)/10),
        n_particles,
        margin,
        h, startSound);
    }
    
    Firework(PVector p, PVector v, int n_particles, float margin, int h, SoundFile startSound) { 
        this.startSound = startSound;
        this.startSound.play(2);
        this.margin = margin;
        if(2 * margin >= width)
            this.margin = 50;
            
        this.pos = p.copy();
        this.v   = v.copy();
        
        this.particle = new Particle(pos, v, gravity);
        this.particles.add(particle);
        this.n_particles = n_particles;
        this.hsb = color(h, 255, 255);
    }

    void update() {
        for (Particle p : particles)
            p.update();
        
        
        if (this.exploded) {
            Iterator i = particles.iterator();
            Particle p;
            while (i.hasNext()) {
                p = (Particle) i.next();
                if (p.pos.y > height)
                    i.remove();
            }
            if(particles.size() == 0){
                startSound.stop();
                endSound.stop();
            }
            return;
        } 
        
        
        if (particles.size() < 6) {
            var p = new Particle(pos, v, gravity);
            particles.add(p);
            p.alpha = 255 - 40 * particles.indexOf(p);
            return;
        }

        if (particle.v.y >= 0 ||
            particle.pos.x <= margin ||
            width - margin <= particle.pos.x ||
            particle.pos.y <= margin) {
                
            var first = particles.get(0);
            particles.clear();
            exploded = true;
            
            for (int i = 0; i < this.n_particles; i++) {
                Particle p = new Particle(first.pos, PVector.random2D().setMag(random(1, 5)), gravity);
                p.alpha = 255 * (random(0, 1) + 0.2);
                particles.add(p);
            }
            startSound.stop();
            endSound.play(2.5);
            return;
        }
    }

    void show() {
        
        for (Particle p : particles) {
            p.show(hsb);
        }
    }
}
