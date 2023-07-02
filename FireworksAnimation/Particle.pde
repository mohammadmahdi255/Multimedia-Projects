class Particle {
  
    PVector pos, v, a;
    float alpha;
  
    Particle(PVector pos, PVector v, PVector g) {
        this.pos = pos.copy();
        this.v = v.copy();
        this.a = g.copy();
        alpha = 255;
    }
  
    void update() {
        this.v.add(this.a);
        this.pos.add(this.v);
    }

    void show(color hsb) {
        stroke(hsb, alpha);
        point(this.pos.x, this.pos.y);
    }
  
    @Override
    Particle clone() {
        return new Particle(pos, v, a);
    }
}
