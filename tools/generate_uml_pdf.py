from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm
from pathlib import Path

OUT = Path("WealthWise_UML_Design_Document.pdf")
NAVY = colors.HexColor("#13213D")
BLUE = colors.HexColor("#4361EE")
PALE = colors.HexColor("#EEF3FF")
TEAL = colors.HexColor("#13A889")
INK = colors.HexColor("#202B3C")
MUTED = colors.HexColor("#68758A")
LINE = colors.HexColor("#D9E1EE")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=30, leading=36, textColor=NAVY, alignment=TA_CENTER, spaceAfter=8))
styles.add(ParagraphStyle(name="Subtitle", parent=styles["Normal"], fontSize=13, leading=19, textColor=MUTED, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="Section", parent=styles["Heading1"], fontSize=22, leading=26, textColor=NAVY, spaceAfter=8))
styles.add(ParagraphStyle(name="Sub", parent=styles["Heading2"], fontSize=12, leading=15, textColor=BLUE, spaceBefore=6, spaceAfter=5))
styles.add(ParagraphStyle(name="BodyWW", parent=styles["BodyText"], fontSize=9.5, leading=14, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="SmallWW", parent=styles["BodyText"], fontSize=8, leading=11, textColor=MUTED))
styles.add(ParagraphStyle(name="Box", parent=styles["BodyText"], fontSize=8.5, leading=11, textColor=INK, alignment=TA_CENTER))

def footer(canvas, doc):
    canvas.saveState()
    w,h=A4
    canvas.setStrokeColor(LINE); canvas.line(18*mm, 15*mm, w-18*mm, 15*mm)
    canvas.setFont("Helvetica", 8); canvas.setFillColor(MUTED)
    canvas.drawString(18*mm, 9*mm, "WEALTHWISE | UML DESIGN DOCUMENT")
    canvas.drawRightString(w-18*mm, 9*mm, f"Page {doc.page}")
    canvas.restoreState()

def box(canvas,x,y,w,h,title,lines,fill=PALE,stroke=BLUE):
    canvas.setFillColor(fill); canvas.setStrokeColor(stroke); canvas.setLineWidth(1)
    canvas.roundRect(x,y,w,h,7,fill=1,stroke=1)
    canvas.setFillColor(NAVY); canvas.setFont("Helvetica-Bold",9)
    canvas.drawCentredString(x+w/2,y+h-15,title)
    canvas.setFillColor(INK); canvas.setFont("Helvetica",7.5)
    yy=y+h-29
    for line in lines:
        canvas.drawCentredString(x+w/2,yy,line); yy-=10

def arrow(c,x1,y1,x2,y2,label=None):
    c.setStrokeColor(MUTED); c.setFillColor(MUTED); c.setLineWidth(1)
    c.line(x1,y1,x2,y2)
    import math
    a=math.atan2(y2-y1,x2-x1); size=5
    c.line(x2,y2,x2-size*math.cos(a-0.5),y2-size*math.sin(a-0.5))
    c.line(x2,y2,x2-size*math.cos(a+0.5),y2-size*math.sin(a+0.5))
    if label:
        c.setFont("Helvetica-Oblique",7); c.drawCentredString((x1+x2)/2,(y1+y2)/2+5,label)

def diagram_page(story,title,subtitle,draw_fn):
    story.append(Paragraph(title,styles["Section"]))
    story.append(Paragraph(subtitle,styles["BodyWW"]))
    story.append(Spacer(1,7))
    from reportlab.platypus import Flowable
    class Figure(Flowable):
        def __init__(self): Flowable.__init__(self); self.width=174*mm; self.height=195*mm
        def draw(self):
            c=self.canv; c.saveState(); draw_fn(c, self.width, self.height); c.restoreState()
    story.append(Figure()); story.append(PageBreak())

def draw_usecase(c,w,h):
    c.setStrokeColor(LINE); c.setLineWidth(1)
    c.roundRect(31,22, w-62,h-40,12,fill=0,stroke=1)
    c.setFillColor(NAVY); c.setFont("Helvetica-Bold",10); c.drawString(43,h-32,"WEALTHWISE SIMULATION")
    # actor
    ax,ay=45,h/2
    c.setStrokeColor(INK); c.circle(ax,ay+28,7,stroke=1,fill=0); c.line(ax,ay+21,ax,ay-1); c.line(ax,ay+14,ax-12,ay+5); c.line(ax,ay+14,ax+12,ay+5); c.line(ax,ay-1,ax-10,ay-17); c.line(ax,ay-1,ax+10,ay-17)
    c.setFont("Helvetica",8); c.drawCentredString(ax,ay-30,"Investor / Student")
    cases=[("View dashboard",h-74),("Browse sample assets",h-111),("Buy virtual units",h-148),("Sell virtual units",h-185),("Review portfolio",h-222),("View transaction history",h-259),("Export CSV",h-296),("Reset simulation",h-333)]
    cx= w*0.67
    for title,y in cases:
        c.setFillColor(PALE); c.setStrokeColor(BLUE); c.ellipse(cx-68,y-13,cx+68,y+13,fill=1,stroke=1)
        c.setFillColor(INK); c.setFont("Helvetica",8); c.drawCentredString(cx,y-3,title)
        arrow(c,ax+14,ay+10,cx-69,y,None)
    c.setFillColor(MUTED); c.setFont("Helvetica-Oblique",8); c.drawString(35,8,"Use cases describe visible user goals; they are not method-level implementation details.")

def draw_class(c,w,h):
    # class blocks centered across page
    box(c, w/2-65,h-80,130,50,"WealthWise",["main() • menu • user interaction"],PALE,BLUE)
    box(c, w/2-65,h-185,130,66,"Portfolio",["cash • holdings • transactions","buy() • sell() • valuation"],colors.HexColor("#E9F8F4"),TEAL)
    box(c,w/2-65,h-285,130,62,"Asset (abstract)",["symbol • name • price","getCategory() • getDescription()"],PALE,BLUE)
    box(c,25,h-390,95,55,"Stock",["extends Asset"],colors.white,TEAL)
    box(c,w-120,h-390,95,55,"MutualFund",["extends Asset"],colors.white,TEAL)
    box(c,w/2-135,35,105,58,"Holding",["units","averageBuyPrice"],colors.white,TEAL)
    box(c,w/2+30,35,115,58,"Transaction",["action • units • price","amount • realized P/L"],colors.white,TEAL)
    arrow(c,w/2,h-80,w/2,h-117,"uses")
    arrow(c,w/2,h-185,w/2,h-223,"contains / values")
    arrow(c,w/2-20,h-285,72,h-335,"inherits")
    arrow(c,w/2+20,h-285,w-72,h-335,"inherits")
    arrow(c,w/2-10,h-185,w/2-80,93,"manages")
    arrow(c,w/2+10,h-185,w/2+85,93,"records")
    c.setFillColor(MUTED); c.setFont("Helvetica-Oblique",8); c.drawString(22,15,"Conceptual class view of the standalone Java companion; nested classes are shown as separate UML boxes.")

def draw_sequence(c,w,h):
    actors=[("Investor",32),("WealthWise",130),("Portfolio",228),("Holding",326),("Transaction",424)]
    top=h-30; bottom=35
    for name,x in actors:
        c.setFillColor(PALE); c.setStrokeColor(BLUE); c.roundRect(x,top-26,70,24,5,fill=1,stroke=1)
        c.setFillColor(NAVY); c.setFont("Helvetica-Bold",8); c.drawCentredString(x+35,top-17,name)
        c.setStrokeColor(LINE); c.setDash(3,3); c.line(x+35,top-26,x+35,bottom); c.setDash()
    steps=[(32,130,"1. select asset + units"),(130,228,"2. request buy(asset, units)"),(228,326,"3. create/update position"),(228,424,"4. record BUY transaction"),(228,130,"5. update cash + totals"),(130,32,"6. show result")]
    y=top-62
    for x1,x2,label in steps:
        arrow(c,x1+35,y,x2+35,y,label)
        y-=36
    c.setFillColor(MUTED); c.setFont("Helvetica-Oblique",8); c.drawString(25,12,"Illustrates a successful buy path; validation may reject invalid quantities or insufficient virtual cash.")

def draw_activity(c,w,h):
    box(c,w/2-55,h-62,110,35,"Start",["user selects Buy"],PALE,BLUE)
    box(c,w/2-77,h-132,154,43,"Validate input",["positive whole units?","enough virtual cash?"],colors.HexColor("#FFF6E5"),colors.HexColor("#D79B30"))
    box(c,20,h-230,115,44,"Reject trade",["show message","state unchanged"],colors.HexColor("#FFF0F0"),colors.HexColor("#D65A63"))
    box(c,w/2-55,h-230,110,44,"Calculate cost",["price × units"],PALE,BLUE)
    box(c,w-135,h-230,115,44,"Update portfolio",["cash / holding","transaction record"],colors.HexColor("#E9F8F4"),TEAL)
    box(c,w/2-55,h-310,110,35,"End",["display result"],PALE,BLUE)
    arrow(c,w/2,h-62,w/2,h-89)
    arrow(c,w/2-25,h-132,78,h-186,"No")
    arrow(c,w/2,h-132,w/2,h-186,"Yes")
    arrow(c,w/2+25,h-132,w-78,h-186,"Yes")
    arrow(c,w/2,h-230,w/2,h-275)
    arrow(c,w-78,h-230,w/2+55,h-290)
    arrow(c,78,h-230,78,h-260,"message")

def draw_components(c,w,h):
    box(c,25,h-95,140,58,"Browser application",["index.html","HTML / CSS / JavaScript"],PALE,BLUE)
    box(c,w-165,h-95,140,58,"Java console program",["WealthWise.java","standalone OOP companion"],colors.HexColor("#E9F8F4"),TEAL)
    box(c,25,h-205,140,58,"Browser storage",["localStorage","simulation state / history"],colors.white,TEAL)
    box(c,w-165,h-205,140,58,"In-memory model",["Asset / Portfolio","Holding / Transaction"],colors.white,TEAL)
    arrow(c,95,h-95,95,h-147,"persists locally")
    arrow(c,w-95,h-95,w-95,h-147,"in-memory state")
    c.setStrokeColor(colors.HexColor("#D65A63")); c.setDash(4,3); c.line(165,h-60,w-165,h-60); c.setDash()
    c.setFillColor(colors.HexColor("#B23B46")); c.setFont("Helvetica-Bold",8); c.drawCentredString(w/2,h-48,"No API or shared-state connection")
    c.setFillColor(MUTED); c.setFont("Helvetica-Oblique",8); c.drawString(22,20,"Deployment/component boundary: the web experience and Java program are separate implementations.")

story=[]
story.append(Spacer(1,42*mm))
story.append(Paragraph("WEALTHWISE",styles["CoverTitle"]))
story.append(Paragraph("UML DESIGN DOCUMENT",styles["CoverTitle"]))
story.append(Spacer(1,5*mm))
story.append(Paragraph("Java OOP Wealth Management & Portfolio Simulator",styles["Subtitle"]))
story.append(Paragraph("NMIMS • MBA Tech AI • OOP Lab",styles["Subtitle"]))
story.append(Spacer(1,20*mm))
cover=Table([[Paragraph("<b>Document contents</b><br/>Use case diagram • Class diagram • Buy sequence diagram • Buy activity diagram • Component / deployment view",styles["BodyWW"])]], colWidths=[150*mm])
cover.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),PALE),("BOX",(0,0),(-1,-1),0.8,BLUE),("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12)]))
story.append(cover); story.append(Spacer(1,18*mm))
story.append(Paragraph("<b>Design boundary:</b> The browser application and Java console program are separate implementations. The Java program does not serve or synchronize with the web page.",styles["BodyWW"]))
story.append(Paragraph("Educational simulation only. Asset names and prices are illustrative; no live market feed or real-money trading is provided.",styles["BodyWW"]))
story.append(PageBreak())
story.append(Paragraph("1. Purpose and Design Boundary",styles["Section"]))
story.append(Paragraph("This document provides five UML-style views of WealthWise. The browser simulation demonstrates the user experience; the standalone Java program demonstrates the object-oriented domain model. Diagrams are conceptual and should be read alongside the actual source code.",styles["BodyWW"]))
story.append(Paragraph("2. System Overview",styles["Section"]))
story.append(Paragraph("The user can browse sample assets, buy or sell virtual units, review portfolio metrics and activity, export CSV data, and reset the simulation. The Java companion models assets, holdings, portfolio operations, and transaction records. There is no API connection between the two implementations.",styles["BodyWW"]))
story.append(Paragraph("3. Diagram Index",styles["Section"]))
story.append(Paragraph("Figure 1 — Use Case Diagram<br/>Figure 2 — Class Diagram<br/>Figure 3 — Buy Asset Sequence Diagram<br/>Figure 4 — Buy Operation Activity Diagram<br/>Figure 5 — Component / Deployment View",styles["BodyWW"]))
story.append(PageBreak())
diagram_page(story,"4. Use Case Diagram","Primary actor: Investor / Student. Use cases represent user-visible goals in the browser simulation.",draw_usecase)
diagram_page(story,"5. Class Diagram","The Java classes below describe the core data model and main relationships in the console companion.",draw_class)
diagram_page(story,"6. Buy Asset Sequence Diagram","Successful buy path from user selection through validation and portfolio updates.",draw_sequence)
diagram_page(story,"7. Buy Operation Activity Diagram","The operation validates units and available cash before updating virtual portfolio state.",draw_activity)
diagram_page(story,"8. Component / Deployment View","Web app stores local state in the browser; Java console has its own in-memory model.",draw_components)
story.append(Paragraph("9. Class Responsibilities and OOP Mapping",styles["Section"]))
rows=[
["Type","Responsibility"],
["WealthWise","Entry point, user menu, asset selection, dashboard output and simulated market movements."],
["Asset (abstract)","Common symbol/name/price fields; category and description are abstract operations."],
["Stock / MutualFund","Concrete asset types overriding category and description."],
["Holding","Units and average buy price; update or remove units while checking quantities."],
["Portfolio","Cash, holdings, transactions, buy/sell validation, valuation and profit/loss calculations."],
["Transaction","Record an action, asset, quantity, unit price, amount, and realized P/L."],
]
tbl=Table([[Paragraph(str(v),styles["SmallWW"]) for v in row] for row in rows],colWidths=[42*mm,120*mm],repeatRows=1)
tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),0.5,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
story.append(tbl); story.append(Spacer(1,8))
story.append(Paragraph("<b>Abstraction:</b> abstract Asset defines shared properties and required behaviours. <b>Inheritance:</b> Stock and MutualFund extend Asset. <b>Polymorphism:</b> overridden methods are called through Asset references. <b>Encapsulation:</b> private fields and controlled methods protect portfolio state. <b>Composition:</b> Portfolio manages Holding and Transaction objects.",styles["BodyWW"]))
story.append(Paragraph("10. Core Rules and Assumptions",styles["Section"]))
story.append(Paragraph("• Quantities must be positive whole numbers.<br/>• A buy is rejected when the available virtual cash is insufficient.<br/>• A sale is rejected when the requested units exceed the held units.<br/>• Purchase cost is unit price multiplied by units.<br/>• Unrealized P/L is current holding value minus invested cost; realized P/L is recorded when units are sold.<br/>• Simulated market movements update illustrative asset prices only.<br/>• No live data, broker connection, authentication, or real trading is implemented.",styles["BodyWW"]))
story.append(Paragraph("11. Notes for Implementation Review",styles["Section"]))
story.append(Paragraph("The UML diagrams are a design aid, not a claim that the web page and Java console application share runtime state. When presenting the project, use the browser application for user-facing behavior and the Java source to explain OOP concepts. Verify the current code and run tests before claiming that any test has passed.",styles["BodyWW"]))
doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=19*mm,leftMargin=19*mm,topMargin=18*mm,bottomMargin=20*mm,title="WealthWise UML Design Document",author="WealthWise Project")
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(f"Wrote {OUT}")
