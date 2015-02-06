import macintoshplus
from PIL import Image
im = Image.open('../vaporwave/1.png')
k=0
im = macintoshplus.insert_pic(macintoshplus.pics[1],im,k=0,x=500,y=650)
im = macintoshplus.insert_pic(macintoshplus.pics[0],im,k=0,x=0,y=300)
im = macintoshplus.insert_pic(macintoshplus.pics[3],im,x=700,y=-100)
im = macintoshplus.insert_pic(macintoshplus.pics[4],im,x=0,y=650)
im = macintoshplus.draw_text('POTSMODERN',im,x=0,y=800, k=93/100)
im.save('mac.png')
