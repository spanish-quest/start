<!DOCTYPE html>
<html>
<head>
    <title>Spanish Quest-Level 3 (Kong)</title>
    <style>
        body { margin: 0; overflow: hidden; background: #000; }
        canvas { display: block; }
    </style>
</head>
<body>
<canvas id="game"></canvas>
<script>
// Game setup
const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 600; // Visible screen height

const levelHeight = 1600;  // Full level height
let cameraY = levelHeight - canvas.height; // Initial camera position

// Game elements
const player = {
    x: 60, y: 740, width: 30, height: 40,  // Start at bottom
    color: '#FF0000',
    speed: 3,   // Slower speed
    isJumping: false,
    jumpPower: 10,  // Reduced jump power
    gravity: 0.5,
    velY: 0,
    velX: 0,
    isClimbing: false,  // Add climbing state
    jumpHoldFrames: 0  // Count frames holding jump
};

const platforms = [
    {x: 0, y: 1540, width: 800, height: 20, color: '#8B4513'}, // Ground floor
    {x: 0, y: 1420, width: 600, height: 20, color: '#8B4513'},
    {x: 200, y: 1300, width: 600, height: 20, color: '#8B4513'},
    {x: 0, y: 1180, width: 600, height: 20, color: '#8B4513'},
    {x: 200, y: 1060, width: 600, height: 20, color: '#8B4513'},
    {x: 0, y: 940, width: 600, height: 20, color: '#8B4513'},
    {x: 200, y: 820, width: 600, height: 20, color: '#8B4513'},
    {x: 0, y: 700, width: 600, height: 20, color: '#8B4513'},
    {x: 200, y: 580, width: 600, height: 20, color: '#8B4513'},
    {x: 0, y: 460, width: 600, height: 20, color: '#8B4513'},
    {x: 200, y: 340, width: 600, height: 20, color: '#8B4513'},
    {x: 0, y: 220, width: 600, height: 20, color: '#8B4513'},
    {x: 0, y: 100, width: 200, height: 20, color: '#8B4513'},  // Left platform for DK
    {x: 600, y: 100, width: 200, height: 20, color: '#8B4513'}   // Right platform for egg
];

const vines = [
  {x: 100, y: 1420, width: 15, height: 120, color: '#228B22', platformY: 1420},
  {x: 300, y: 1300, width: 15, height: 120, color: '#228B22', platformY: 1300},
  {x: 500, y: 1180, width: 15, height: 120, color: '#228B22', platformY: 1180},
  {x: 200, y: 1060, width: 15, height: 120, color: '#228B22', platformY: 1060},
  {x: 400, y: 940, width: 15, height: 120, color: '#228B22', platformY: 940},
  {x: 100, y: 820, width: 15, height: 120, color: '#228B22', platformY: 820},
  {x: 500, y: 700, width: 15, height: 120, color: '#228B22', platformY: 700},
  {x: 100, y: 580, width: 15, height: 120, color: '#228B22', platformY: 580},
  {x: 300, y: 460, width: 15, height: 120, color: '#228B22', platformY: 460},
  {x: 400, y: 340, width: 15, height: 120, color: '#228B22', platformY: 340},
  {x: 100, y: 220, width: 15, height: 120, color: '#228B22', platformY: 220}
];

const mosquitoFires = [
    {x: 60, y: 1520, width: 30, height: 30, active: true}
];

let boulders = [];

// Load Donkey Kong image (even though he's off-screen)
const dkImage = new Image();
dkImage.src = 'https://cdn.viva.org.uk/wp-content/uploads/2022/06/Brown-Howler-Monkey.png';

let donkeyKong = {x: 100, y: 40, width: 100, height: 100}; // Stays at the top

// The Egg (Princess)
let egg = {x: 700, y: 40, width: 30, height: 40}; // Top

// Controls
const keys = {
    ArrowLeft: false,
    ArrowRight: false,
    ArrowUp: false,
    ArrowDown: false // Add down arrow for climbing down
};

document.addEventListener('keydown', (e) => keys[e.key] = true);
document.addEventListener('keyup', (e) => keys[e.key] = false);

// Game functions
function drawDonkeyKong() {
    // Only draw if within the visible screen
    if (donkeyKong.y + donkeyKong.height > cameraY && donkeyKong.y < cameraY + canvas.height) {
        ctx.drawImage(dkImage, donkeyKong.x, donkeyKong.y - cameraY, donkeyKong.width, donkeyKong.height);
    }
}

function drawMosquitoFire(x, y) {
    ctx.fillStyle = '#333';
    ctx.beginPath();
    ctx.ellipse(x + 15, y + 15, 10, 5, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#555';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(x + 10, y + 10);
    ctx.lineTo(x + 5, y);
    ctx.moveTo(x + 20, y + 10);
    ctx.lineTo(x + 25, y);
    ctx.stroke();
}

function checkPlatformCollision() {
    //Platform collisions will happen from all sides
    platforms.forEach(platform => {
        if (player.x + player.width > platform.x &&
            player.x < platform.x + platform.width) {
            // Top Collision
            if (player.y + player.height >= platform.y && player.y + player.height <= platform.y + 10 && player.velY >= 0) {
                player.y = platform.y - player.height;
                player.velY = 0;
                player.isJumping = false;  // Reset isJumping on landing
            }
            // Bottom Collision
            else if (player.y <= platform.y + platform.height && player.y >= platform.y + platform.height - 10 && player.velY <= 0) {
                player.y = platform.y + platform.height;
                player.velY = 0;
            }
        }
    });
}

function checkVineCollision() {
    player.canClimb = false;
    vines.forEach(vine => {
        if (player.x + player.width > vine.x &&
            player.x < vine.x + vine.width &&
            player.y + player.height > vine.y &&
            player.y < vine.y + vine.height &&
            player.y + player.height === vine.platformY) {
            player.canClimb = true;
        }
    });
}

function throwBoulder() {
    if (Math.random() < 0.01) {
        boulders.push({
            x: donkeyKong.x + 30,
            y: donkeyKong.y + 70,
            radius: 15,
            velX: -2 - Math.random() * 2,
            velY: 0
        });
    }
}

function updateBoulders() {
    for (let i = boulders.length - 1; i >= 0; i--) {
        const b = boulders[i];
        b.x += b.velX;
        b.y += b.velY;
        b.velY += 0.2;

        // Bounce off walls
        if (b.x - b.radius < 0 || b.x + b.radius > canvas.width) {
            b.velX *= -1;
        }
            
        // Check for platform collision
        platforms.forEach(platform => {
            if (b.y + b.radius > platform.y &&
                b.y < platform.y + platform.height &&
                b.x > platform.x &&
                b.x < platform.x + platform.width) {
                b.y = platform.y - b.radius;
                b.velY *= -0.5;
                b.velX *= 1; //Setting it to a value greater than 0 would keep it moving

            }
        });

        // Remove if off screen (below the level)
        if (b.y > levelHeight) boulders.splice(i, 1);

        // Player collision check
        const distX = Math.abs(b.x - (player.x + player.width/2));
        const distY = Math.abs(b.y - (player.y + player.height/2));
        if (distX < b.radius + player.width/2 && distY < b.radius + player.height/2) {
            alert('Game Over! Hit by a boulder!');
            resetGame();
        }
    }
}

function checkEggCollision() {
    if (player.x + player.width > egg.x &&
        player.x < egg.x + egg.width &&
        player.y + player.height > egg.y &&
        player.y < egg.y + egg.height) {
        window.location.href = 'cut_finale.html';
    }
}

function resetGame() {
    player.x = 60;
    player.y = 740;  // Reset at bottom
    player.velY = 0;
    boulders = [];
}

// Draw the egg at the top
function drawEgg(x, y) {
    ctx.fillStyle = '#FFFF00';
    ctx.beginPath();
    ctx.ellipse(x + 15, y + 20, 15, 20, 0, 0, Math.PI * 2);
    ctx.fill();
}

// Main game loop
function gameLoop() {
    // Player movement
    if (keys.ArrowLeft) player.x -= player.speed;
    if (keys.ArrowRight) player.x += player.speed;

    // Jumping (realistic physics)
    if (keys.ArrowUp) {
        if (!player.isJumping) {
            player.velY = -player.jumpPower;
            player.isJumping = true;
            player.jumpHoldFrames = 0;  // Reset frames when jumping
        } else if (player.jumpHoldFrames < 10) {  // Allow holding for a few frames
            player.velY -= 0.3;  // Add a bit of extra upwards velocity
            player.jumpHoldFrames++;
        }
    } else {
        player.jumpHoldFrames = 0;  // Reset when not holding jump
    }

    // Climbing vines
    checkVineCollision();
    if (player.canClimb && keys.ArrowUp) { // Only climb if touching vine AND holding up
        player.isClimbing = true;  // Flag that we're actively climbing
        player.y -= 1;  // Slow climbing speed
    } else {
        player.isClimbing = false;  // Stop climbing if no key is pressed or not on vine
    }
    
    // Apply gravity
    player.velY += player.gravity;
    player.y += player.velY;

    // Platform collision
    checkPlatformCollision();

    // Boulders
    throwBoulder();
    updateBoulders();

    // Check Egg Collision
    checkEggCollision();

    // Boundaries
    if (player.x < 0) player.x = 0;
    if (player.x + player.width > canvas.width) player.x = canvas.width - player.width;
    if (player.y > levelHeight) {
        resetGame(); // Fall off the bottom, reset.
    }

    // Update camera position to follow player (scrolling)
    cameraY = player.y - canvas.height / 2;
    if (cameraY < 0) cameraY = 0; // Keep camera within bounds
    if (cameraY > levelHeight - canvas.height) cameraY = levelHeight - canvas.height;

    // Clear screen
    ctx.fillStyle = '#1A3D1A';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw platforms
    platforms.forEach(platform => {
        if (platform.y > cameraY && platform.y < cameraY + canvas.height) {
            ctx.fillStyle = platform.color;
            ctx.fillRect(platform.x, platform.y - cameraY, platform.width, platform.height);
        }
    });

    // Draw vines
    vines.forEach(vine => {
        if (vine.y > cameraY && vine.y < cameraY + canvas.height) {
            ctx.fillStyle = vine.color;
            ctx.fillRect(vine.x, vine.y - cameraY, vine.width, vine.height);
            // Draw vine texture
            ctx.strokeStyle = '#2E8B57';
            for (let y = vine.y - cameraY; y < vine.y - cameraY + vine.height; y += 10) {
                ctx.beginPath();
                ctx.moveTo(vine.x, y);
                ctx.lineTo(vine.x + vine.width, y);
                ctx.stroke();
            }
        }
    });

    // Draw mosquito fires
    mosquitoFires.forEach(fire => {
        if (fire.active && fire.y > cameraY && fire.y < cameraY + canvas.height) {
            drawMosquitoFire(fire.x, fire.y - cameraY);
        }
    });

    // Draw boulders
    boulders.forEach(b => {
        if (b.y > cameraY && b.y < cameraY + canvas.height) {
            ctx.fillStyle = '#777';
            ctx.beginPath();
            ctx.arc(b.x, b.y - cameraY, b.radius, 0, Math.PI * 2);
            ctx.fill();
        }
    });

    // Draw Donkey Kong
    drawDonkeyKong();

    // Draw egg
    if (egg.y > cameraY && egg.y < cameraY + canvas.height) {
        drawEgg(egg.x, egg.y - cameraY);
    }

    // Draw player (red cube)
    ctx.fillStyle = player.color;
    ctx.fillRect(player.x, player.y - cameraY, player.width, player.height);

    requestAnimationFrame(gameLoop);
}

dkImage.onload = gameLoop; // Start game once DK image is loaded
</script>
</body>
</html>
