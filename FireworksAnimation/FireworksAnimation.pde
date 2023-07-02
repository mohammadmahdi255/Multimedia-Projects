import processing.sound.*;
import java.util.Iterator;

ArrayList<Firework> fireworks = new ArrayList<Firework>();
PVector gravity;

int margin = 30;
int x = margin;

long holdTime = 0;

String bang = "bang.wav";
String whooshes = "whooshes.wav";

SoundFile whooshesFile;

volatile boolean isClicked;
volatile char pressedKey = '\0';

void setup() {
    size(1200, 900);
    colorMode(HSB);
    stroke(255);
    strokeWeight(5);
          
    gravity = new PVector(0, 0.2);
}

void draw() {
    background(0, 0, 0, 255);
    
    
    
    if (isClicked) {
        Firework f = new Firework(new PVector(mouseX, mouseY),
        new PVector(random(-50, 50)/10, - (min((holdTime * 0.02), 25))),
        round(random(100, 150)),
        margin,
        round(random(0,2550) / 10),
        new SoundFile(this, whooshes)
        );
        f.endSound = new SoundFile(this, bang);
        fireworks.add(f);
        isClicked = false;
        holdTime = 0;
    } else if (pressedKey == '1') {
        int count = round(random(10, 20));
        for(int i = 0; i < count ; i++) {
            Firework f = new Firework(round(random(100, 150)), margin, round(random(0, 2550) / 10), new SoundFile(this, whooshes));
            f.endSound = new SoundFile(this, bang);
            fireworks.add(f); 
        }
        pressedKey = '\0';
    } else if(pressedKey == '2') {
        Firework f = new Firework(width - x, height, round(random(100, 150)), margin, round(random(0, 2550) / 10), new SoundFile(this, whooshes));
        f.endSound = new SoundFile(this, bang);
        fireworks.add(f);
        x += 30;
        if (x >= width - margin) {
            x = margin;
            pressedKey = '\0';
        }
    } else if(pressedKey == '3') {
        Firework f = new Firework(x, height, round(random(100, 150)), margin, round(random(0, 2550) / 10), new SoundFile(this, whooshes));
        f.endSound = new SoundFile(this, bang);
        fireworks.add(f);
        x += 30;
        if (x >= width - margin) {
            x = margin;
            pressedKey = '\0';
        }
    } else if (random(0, 1) < 0.015) {
        Firework f = new Firework(round(random(100, 150)), margin, round(random(0, 2550) / 10), new SoundFile(this, whooshes));
        f.endSound = new SoundFile(this, bang);
        fireworks.add(f);  
    }
    
    Iterator i = fireworks.iterator();
    Firework f;
    while (i.hasNext()) {
        f = (Firework) i.next();
        if (f.particles.size() < 1) {
            i.remove();
        } else {
            f.update();
            f.show();
        }
    }
    
}

void mousePressed() {
    if (holdTime == 0) {
        holdTime = millis();
    }
}

void mouseReleased() {
    if (!isClicked) {
        holdTime = millis() - holdTime;
        isClicked = true;
    }
}

void keyTyped() {
    if (pressedKey == '\0')
        pressedKey = key;
}
