# colorgram.py

**colorgram.py** is a Python library that lets you extract colors from
images. Compared to other libraries, the colorgram algorithm's results
are more intense.

colorgram.py is a port of
[colorgram.js](https://github.com/darosh/colorgram-js), a JavaScript
library written by GitHub user [@darosh](https://github.com/darosh). The
goal is to have 100% accuracy to the results of the original library (a
goal that is met). I decided to port it since I much prefer the results
the colorgram algorithm gets over those of alternative libraries - have
a look in the next section.

## Results

![Results of colorgram.py on a 512x512
image](http://i.imgur.com/BeReaRM.png)

Time-wise, an extraction of a 512x512 image takes about 0.66s (another
popular color extraction library, [Color
Thief](https://github.com/fengsp/color-thief-py), takes about 1.05s).

## Installation

You can install colorgram.py with
[pip](https://pip.pypa.io/en/latest/installing/), as following:

    pip install colorgram.py

## How to use

Using colorgram.py is simple. Mainly there's only one function you'll
need to use - `colorgram.extract`.

### Example

``` python
import colorgram

# Extract 6 colors from an image.
colors = colorgram.extract('sweet_pic.jpg', 6)

# colorgram.extract returns Color objects, which let you access
# RGB, HSL, and what proportion of the image was that color.
first_color = colors[0]
rgb = first_color.rgb # e.g. (255, 151, 210)
hsl = first_color.hsl # e.g. (230, 255, 203)
proportion  = first_color.proportion # e.g. 0.34

# RGB and HSL are named tuples, so values can be accessed as properties.
# These all work just as well:
red = rgb[0]
red = rgb.r
saturation = hsl[1]
saturation = hsl.s
```

### `colorgram.extract(image, number_of_colors)`

Extract colors from an image. `image` may be either a path to a file, a
file-like object, or a Pillow `Image` object. The function will return a
list of `number_of_colors` `Color` objects.

### `colorgram.Color`

A color extracted from an image. Its properties are:

  - `Color.rgb` - The color represented as a `namedtuple` of RGB from 0
    to 255, e.g. `(r=255, g=151, b=210)`.
  - `Color.hsl` - The color represented as a `namedtuple` of HSL from 0
    to 255, e.g. `(h=230, s=255, l=203)`.
  - `Color.proportion` - The proportion of the image that is in the
    extracted color from 0 to 1, e.g. `0.34`.


#### Docker for API

You can build and run the docker using the following process:

Cloning
```console
git clone https://github.com/jqueguiner/colorgram.git colorgramd
```

Building Docker
```console
cd colorgram && docker build -t colorgram -f Dockerfile-api .
```

Running Docker
```console
echo "http://$(curl ifconfig.io):5000" && docker run -p 5000:5000 -d colorgram
```

Calling the API for image detection
```console
curl -X POST "http://MY_SUPER_API_IP:5000/detect" -H "accept: image/png" -H "Content-Type: application/json" -d '{"url":"https://i.ibb.co/pPPwSdq/input.jpg"}'
```


### Sorting by HSL

Something the original library lets you do is sort the colors you get by
HSL. In actuality, though, the colors are only sorted by hue (as of
colorgram.js 0.1.5), while saturation and lightness are ignored. To get
the corresponding result in colorgram.py, simply do:

``` python
colors.sort(key=lambda c: c.hsl.h)
# or...
sorted(colors, key=lambda c: c.hsl.h)
```

Contact ---
