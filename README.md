# PaperPad
PaperPad is an application that makes digital drawing less expensive, more convenient, and increases worker productivity and time-efficiency.

# Inspiration
Our team was inspired to create this project when we realized that there were many problems with all digital drawing solutions. Currently, if you want to draw digitally, whether that be professionally or for a hobby, you would have to buy a drawing tablet or an iPad. With PaperPad, we solved all of those problems with currently all other digital drawing solutions.

The first common problem we solved is that drawing tablets and iPads are very expensive, costing in the hundreds of dollars. This makes them inaccessible for many artists, students, and hobbyists. However, PaperPad solves this problem. With PaperPad, all you need is a cheap $20 webcam and a piece of paper.

The second common problem we solved is that drawing tablets and iPads don’t feel like real paper. Additionally, you’re forced to draw using a company’s proprietary drawing tools such as the Wacom Pen or the Apple Pencil, which barely feel like normal pencils. As a result, there’s a large learning curve to being good at drawing digitally versus being good at drawing on physical paper. This is such a massive problem that drawing tablet manufacturers and iPad accessory companies tout their products as having a “paper feel.” Many of them even offer “paper special editions” where the only difference is that the product feels more like paper than their other products. With PaperPad, you’ll have no such problem or learning curve. Nothing feels more like pencil and paper than a real pencil and real paper!

PaperPad is also really easy to monetize! Since PaperPad only uses a cheap webcam and a piece of paper, we don’t need to ship any special hardware to customers. All customers have to do is download our software and pay for a subscription. I hope to turn PaperPad into a business after this hackathon.

# What it does
PaperPad allows you to draw digitally with just a cheap $20 webcam and a piece of paper. This makes it more accessible, more convenient, and more portable than existing digital drawing solutions such as Wacom drawing tablets and iPads.
PaperPad uses computer vision to detect, locate, isolate, and locate your hand. It then uses a few complex algorithms to locate the tip of the pencil you are holding. PaperPad then uses that information to control mouse movement, clicking, and dragging, allowing you to draw digitally. As a result, PaperPad is compatible with all apps ⁠— something that’s not true for many other current digital drawing solutions.

# How we built it
First, we used opencv for computer vision, so that we could detect, locate and isolate the user’s hands. Then we use a few complex computer vision algorithms to locate the tip of the pencil you are holding. Finally, we take that data and use it to control mouse movement, clicking, and dragging — allowing you to draw digitally.

# Challenges we ran into
We had some issues locating the hand and the position of the pen/pencil tip. Often, it would be too sensitive, but eventually we managed to fix the issue. At first, we had major latency issues, but we fixed that by heavily optimizing our computer vision code.

# Accomplishments that we're proud of
We are proud that we got the opencv computer vision hand and pen tip detection and mapping working very accurately, almost perfectly.

# What we learned
Our team learned how to use opencv, combined with image processing techniques, in order to detect, isolate, and map hands and fingers, as well as their shapes and positions.

# What's next for PaperPad
Our team would like to further improve the accuracy of the computer vision hand and pen tip detection. Finally, we are interested in polishing the project and **selling it as a subscription** online. PaperPad has **business potential** in a large market since it makes digital drawing significantly cheaper, and therefore more accessible and more convenient for people around the world. Additionally, PaperPad will **improve worker productivity and time-efficiency** for professional artists and graphic designers since PaperPad provides a better user experience — a drawing tool and a drawing surface that is a real pencil and real paper instead of just “feeling like pencil and paper” like many other digital drawing solutions from many companies.