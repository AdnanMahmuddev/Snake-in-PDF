PDF_FILE_TEMPLATE = """
%PDF-1.6

% Root
1 0 obj
<<
  /AcroForm <<
    /Fields [ ###FIELD_LIST### ]
  >>
  /Pages 2 0 R
  /OpenAction 17 0 R
  /Type /Catalog
>>
endobj

2 0 obj
<<
  /Count 1
  /Kids [
    16 0 R
  ]
  /Type /Pages
>>

%% Annots Page 1 (also used as overall fields list)
21 0 obj
[
  ###FIELD_LIST###
]
endobj

###FIELDS###

%% Page 1
16 0 obj
<<
  /Annots 21 0 R
  /Contents 3 0 R
  /CropBox [
    0.0
    0.0
    612.0
    792.0
  ]
  /MediaBox [
    0.0
    0.0
    612.0
    792.0
  ]
  /Parent 2 0 R
  /Resources <<
  >>
  /Rotate 0
  /Type /Page
>>
endobj

3 0 obj
<< >>
stream
endstream
endobj

17 0 obj
<<
  /JS 42 0 R
  /S /JavaScript
>>
endobj

42 0 obj
<< >>
stream
// Simple Snake game in PDF JavaScript

var GRID_WIDTH = ###GRID_WIDTH###;
var GRID_HEIGHT = ###GRID_HEIGHT###;
var TICK_INTERVAL = 150;

var pixel_fields = [];
var snake = [{x: Math.floor(GRID_WIDTH/2), y: Math.floor(GRID_HEIGHT/2)}];
var direction = {x: 0, y: -1};
var food = null;
var interval = null;
var score = 0;

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}

function spawn_food() {
  var valid = false;
  var fx, fy;
  while (!valid) {
    fx = randomInt(0, GRID_WIDTH);
    fy = randomInt(0, GRID_HEIGHT);
    valid = true;
    for (var i=0; i<snake.length; i++) {
      if (snake[i].x == fx && snake[i].y == fy) {
        valid = false;
        break;
      }
    }
  }
  food = {x: fx, y: fy};
}

function set_pixel(x, y, state) {
  if (x < 0 || y < 0 || x >= GRID_WIDTH || y >= GRID_HEIGHT) return;
  pixel_fields[x][y].hidden = !state;
}

function draw() {
  // Clear all
  for (var x=0; x<GRID_WIDTH; x++) {
    for (var y=0; y<GRID_HEIGHT; y++) {
      set_pixel(x, y, false);
    }
  }
  // Draw snake
  for (var i=0; i<snake.length; i++) {
    set_pixel(snake[i].x, snake[i].y, true);
  }
  // Draw food
  if (food) set_pixel(food.x, food.y, true);
  this.getField("T_score").value = "Score: " + score;
}

function game_over() {
  app.clearInterval(interval);
  app.alert("Game Over! Score: " + score + "\\nRefresh to restart.");
  set_controls_visibility(false);
  this.getField("B_start").hidden = false;
}

function set_controls_visibility(state) {
  this.getField("B_up").hidden = !state;
  this.getField("B_down").hidden = !state;
  this.getField("B_left").hidden = !state;
  this.getField("B_right").hidden = !state;
}

function game_tick() {
  var new_head = {x: snake[0].x + direction.x, y: snake[0].y + direction.y};

  // Wrap around logic for borders
  if (new_head.x < 0) {
    new_head.x = GRID_WIDTH - 1;
  } else if (new_head.x >= GRID_WIDTH) {
    new_head.x = 0;
  }

  if (new_head.y < 0) {
    new_head.y = GRID_HEIGHT - 1;
  } else if (new_head.y >= GRID_HEIGHT) {
    new_head.y = 0;
  }

  // Check collision with self
  for (var i=0; i<snake.length; i++) {
    if (snake[i].x == new_head.x && snake[i].y == new_head.y) {
      game_over();
      return;
    }
  }

  snake.unshift(new_head);

  // Check if food eaten
  if (food && new_head.x == food.x && new_head.y == food.y) {
    score++;
    spawn_food();
  } else {
    snake.pop();
  }

  draw();
}

function start_game() {
  snake = [{x: Math.floor(GRID_WIDTH/2), y: Math.floor(GRID_HEIGHT/2)}];
  direction = {x: 0, y: -1};
  score = 0;
  spawn_food();
  draw();
  set_controls_visibility(true);
  this.getField("B_start").hidden = true;
  interval = app.setInterval("game_tick();", TICK_INTERVAL);
}

function move_up() {
  if (direction.y != 1) direction = {x:0, y:-1};
}

function move_down() {
  if (direction.y != -1) direction = {x:0, y:1};
}

function move_left() {
  if (direction.x != 1) direction = {x:-1, y:0};
}

function move_right() {
  if (direction.x != -1) direction = {x:1, y:0};
}

// Initialize pixel_fields array
function init_fields() {
  for (var x=0; x<GRID_WIDTH; x++) {
    pixel_fields[x] = [];
    for (var y=0; y<GRID_HEIGHT; y++) {
      pixel_fields[x][y] = this.getField("P_" + x + "_" + y);
    }
  }
}

// On document open
init_fields();
set_controls_visibility(false);

endstream
endobj

18 0 obj
<<
  /JS 43 0 R
  /S /JavaScript
>>
endobj

43 0 obj
<< >>
stream
// Empty secondary JS stream
endstream
endobj

trailer
<<
  /Root 1 0 R
>>

%%EOF
"""

PLAYING_FIELD_OBJ = """
###IDX### obj
<<
  /FT /Btn
  /Ff 1
  /MK <<
    /BG [0.8]
    /BC [0 0 0]
  >>
  /Border [0 0 1]
  /P 16 0 R
  /Rect [###RECT###]
  /Subtype /Widget
  /T (playing_field)
  /Type /Annot
>>
endobj
"""

PIXEL_OBJ = """
###IDX### obj
<<
  /FT /Btn
  /Ff 1
  /MK <<
    /BG [###COLOR###]
    /BC [0.5 0.5 0.5]
  >>
  /Border [0 0 1]
  /P 16 0 R
  /Rect [###RECT###]
  /Subtype /Widget
  /T (P_###X###_###Y###)
  /Type /Annot
>>
endobj
"""

BUTTON_AP_STREAM = """
###IDX### obj
<<
  /BBox [0.0 0.0 ###WIDTH### ###HEIGHT###]
  /FormType 1
  /Matrix [1.0 0.0 0.0 1.0 0.0 0.0]
  /Resources <<
    /Font << /HeBo 10 0 R >>
    /ProcSet [ /PDF /Text ]
  >>
  /Subtype /Form
  /Type /XObject
>>
stream
q
0.75 g
0 0 ###WIDTH### ###HEIGHT### re
f
Q
q
1 1 ###WIDTH### ###HEIGHT### re
W
n
BT
/HeBo 12 Tf
0 g
10 8 Td
(###TEXT###) Tj
ET
Q
endstream
endobj
"""

BUTTON_OBJ = """
###IDX### obj
<<
  /A <<
    /JS ###SCRIPT_IDX### R
    /S /JavaScript
  >>
  /AP << /N ###AP_IDX### R >>
  /F 4
  /FT /Btn
  /Ff 65536
  /MK << /BG [0.75] /CA (###LABEL###) >>
  /P 16 0 R
  /Rect [###RECT###]
  /Subtype /Widget
  /T (###NAME###)
  /Type /Annot
>>
endobj
"""

TEXT_OBJ = """
###IDX### obj
<<
  /AA << /K << /JS ###SCRIPT_IDX### R /S /JavaScript >> >>
  /F 4
  /FT /Tx
  /MK << >>
  /MaxLen 0
  /P 16 0 R
  /Rect [###RECT###]
  /Subtype /Widget
  /T (###NAME###)
  /V (###LABEL###)
  /Type /Annot
>>
endobj
"""

STREAM_OBJ = """
###IDX### obj
<< >>
stream
###CONTENT###
endstream
endobj
"""

PX_SIZE = 20
GRID_WIDTH = 15
GRID_HEIGHT = 15
GRID_OFF_X = 200
GRID_OFF_Y = 400

fields_text = ""
field_indexes = []
obj_idx_ctr = 50

def add_field(field):
    global fields_text, field_indexes, obj_idx_ctr
    fields_text += field
    field_indexes.append(obj_idx_ctr)
    obj_idx_ctr += 1

# Playing field outline (no visible color)
playing_field = PLAYING_FIELD_OBJ.replace("###IDX###", f"{obj_idx_ctr} 0")
playing_field = playing_field.replace("###RECT###", f"{GRID_OFF_X} {GRID_OFF_Y} {GRID_OFF_X + GRID_WIDTH*PX_SIZE} {GRID_OFF_Y + GRID_HEIGHT*PX_SIZE}")
add_field(playing_field)

# Create pixels
for x in range(GRID_WIDTH):
    for y in range(GRID_HEIGHT):
        pixel = PIXEL_OBJ.replace("###IDX###", f"{obj_idx_ctr} 0")
        # White pixel background means off (hidden), so use white
        pixel = pixel.replace("###COLOR###", "1 1 1")
        pixel = pixel.replace("###RECT###", f"{GRID_OFF_X + x*PX_SIZE} {GRID_OFF_Y + y*PX_SIZE} {GRID_OFF_X + (x+1)*PX_SIZE} {GRID_OFF_Y + (y+1)*PX_SIZE}")
        pixel = pixel.replace("###X###", str(x))
        pixel = pixel.replace("###Y###", str(y))
        add_field(pixel)

# Add buttons function
def add_button(label, name, x, y, width, height, js):
    global obj_idx_ctr, fields_text, field_indexes

    # JS script object
    script = STREAM_OBJ.replace("###IDX###", f"{obj_idx_ctr} 0").replace("###CONTENT###", js)
    add_field(script)

    # Appearance stream
    ap_stream = BUTTON_AP_STREAM.replace("###IDX###", f"{obj_idx_ctr} 0")
    ap_stream = ap_stream.replace("###TEXT###", label)
    ap_stream = ap_stream.replace("###WIDTH###", str(width))
    ap_stream = ap_stream.replace("###HEIGHT###", str(height))
    add_field(ap_stream)

    # Button object itself
    button = BUTTON_OBJ.replace("###IDX###", f"{obj_idx_ctr} 0")
    button = button.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-2} 0")
    button = button.replace("###AP_IDX###", f"{obj_idx_ctr-1} 0")
    button = button.replace("###LABEL###", label)
    button = button.replace("###NAME###", name)
    button = button.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
    add_field(button)

# Add directional buttons (Up, Down, Left, Right)
add_button("↑", "B_up", GRID_OFF_X + 60, GRID_OFF_Y - 60, 50, 50, "move_up();")
add_button("↓", "B_down", GRID_OFF_X + 60, GRID_OFF_Y - 10, 50, 50, "move_down();")
add_button("←", "B_left", GRID_OFF_X + 10, GRID_OFF_Y - 35, 50, 50, "move_left();")
add_button("→", "B_right", GRID_OFF_X + 110, GRID_OFF_Y - 35, 50, 50, "move_right();")

# Add Start button
add_button("Start", "B_start",
           GRID_OFF_X + (GRID_WIDTH * PX_SIZE) // 2 - 40,
           GRID_OFF_Y + (GRID_HEIGHT * PX_SIZE) // 2 - 40,
           80, 80, "start_game();")

# Add score text field function
def add_text(label, name, x, y, width, height, js):
    global obj_idx_ctr, fields_text, field_indexes
    script = STREAM_OBJ.replace("###IDX###", f"{obj_idx_ctr} 0").replace("###CONTENT###", js)
    add_field(script)
    text = TEXT_OBJ.replace("###IDX###", f"{obj_idx_ctr} 0")
    text = text.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-1} 0")
    text = text.replace("###LABEL###", label)
    text = text.replace("###NAME###", name)
    text = text.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
    add_field(text)

# Add Score text field on right of grid
add_text("Score: 0", "T_score",
         GRID_OFF_X + GRID_WIDTH * PX_SIZE + 10,
         GRID_OFF_Y + GRID_HEIGHT * PX_SIZE - 40,
         100, 30, "")

# Replace placeholders in PDF template
filled_pdf = PDF_FILE_TEMPLATE.replace("###FIELDS###", fields_text)
filled_pdf = filled_pdf.replace("###FIELD_LIST###", " ".join([f"{i} 0 R" for i in field_indexes]))
filled_pdf = filled_pdf.replace("###GRID_WIDTH###", str(GRID_WIDTH))
filled_pdf = filled_pdf.replace("###GRID_HEIGHT###", str(GRID_HEIGHT))

# Write the PDF content to file
with open("snake_game.pdf", "w", encoding="utf-8") as f:
    f.write(filled_pdf)

print("snake_game.pdf generated successfully.")
