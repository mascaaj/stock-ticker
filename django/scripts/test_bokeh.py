from bokeh.embed import components
from bokeh.plotting import figure, show, output_file

# The figure will be rendered in a static HTML file called output_file_test.html
# output_file('output_file_test.html', 
#             title='Empty Bokeh Figure')

# My x-y coordinate data
x = [1, 2, 1]
y = [1, 1, 2]

# Create a figure with no toolbar and axis ranges of [0,3]
fig = figure(title='My Coordinates',
             plot_height=300, plot_width=300,
             x_range=(0, 3), y_range=(0, 3),
             toolbar_location=None)

# Draw the coordinates as circles
fig.circle(x=x, y=y,
           color='green', size=10, alpha=0.5)

# See what it looks like
show(fig)
# script, div = components(fig)