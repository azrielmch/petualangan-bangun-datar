"""Exact complementary jigsaw outlines for 4–8 pieces, including odd counts."""

LEVELS=[('segitiga',4,2),('persegi',4,2),('lingkaran',6,3),('persegi-panjang',6,3),('segi-lima',8,4)]

def make_layout(shape,count,cols,level):
    rows=2;cw=480/cols;ch=360/rows
    regions=[{(x,y)} for y in range(rows) for x in range(cols)]
    if count%2:
        # Join two neighboring cells; the perimeter remains a real jigsaw.
        regions[-2]|=regions[-1];regions.pop()
    pieces=[]
    for index,cells in enumerate(regions):
        edges={}
        for x,y in cells:
            for neighbor,a,b in [((x,y-1),(x,y),(x+1,y)),((x+1,y),(x+1,y),(x+1,y+1)),((x,y+1),(x+1,y+1),(x,y+1)),((x-1,y),(x,y+1),(x,y))]:
                if neighbor not in cells:edges[a]=b
        start=min(edges,key=lambda p:(p[1],p[0]));a=start
        commands=[f'M{a[0]*cw:g} {a[1]*ch:g}'];shared=[]
        while True:
            b=edges[a];ax,ay=a[0]*cw,a[1]*ch;bx,by=b[0]*cw,b[1]*ch
            horizontal=a[1]==b[1]
            outside=(horizontal and a[1] in (0,rows)) or (not horizontal and a[0] in (0,cols))
            if outside:commands.append(f'L{bx:g} {by:g}')
            else:
                sign=1 if (min(a[0],b[0])+min(a[1],b[1]))%2==0 else -1
                nx,ny=(0,sign) if horizontal else (sign,0)
                def p(t,d=0):return f'{ax+(bx-ax)*t+nx*d:g} {ay+(by-ay)*t+ny*d:g}'
                commands.extend(['L'+p(.35),'C'+p(.42)+' '+p(.36,18)+' '+p(.5,18),'C'+p(.64,18)+' '+p(.58)+' '+p(.65),f'L{bx:g} {by:g}'])
                shared.append({'edge':[list(min(a,b)),list(max(a,b))],'direction':1 if a<b else -1})
            a=b
            if a==start:break
        commands.append('Z')
        xs=[x*cw for x,y in cells];ys=[y*ch for x,y in cells]
        left=max(0,min(xs)-18);top=max(0,min(ys)-18)
        right=min(480,max(xs)+cw+18);bottom=min(360,max(ys)+ch+18)
        pieces.append({'id':index,'path':' '.join(commands),'targetX':min(xs),'targetY':min(ys),'bounds':{'x':left,'y':top,'width':right-left,'height':bottom-top},'cells':[list(c) for c in sorted(cells)],'sharedEdges':shared})
    return {'level':level,'shape':shape,'pieceCount':count,'width':480,'height':360,'rows':rows,'columns':cols,'pieces':pieces}

def all_layouts():
    return [make_layout(shape,count,cols,i+1) for i,(shape,count,cols) in enumerate(LEVELS)]
