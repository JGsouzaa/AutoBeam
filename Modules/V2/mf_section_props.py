from mr_project import *
#gets section properties from bar element
def get_height(barNumber):
    barObject = IRobotBar(bars.Get(barNumber))
    barLabel = IRobotLabel(barObject.GetLabel(3))
    sectionheight = IRobotBarSectionData(barLabel.Data).GetValue(12)
    return(sectionheight)
def get_width(barNumber):
    barObject = IRobotBar(bars.Get(barNumber))
    barLabel = IRobotLabel(barObject.GetLabel(3))
    sectionwidth = IRobotBarSectionData(barLabel.Data).GetValue(13)
    return(sectionwidth)

def retangularInertia(barNumber):
    inertia = {}
    width = inertiaWidth(barNumber)
    height = inertiaHeight(barNumber)
    inertia["Iy"] = width
    inertia["Ix"] = height

    def inertiaWidth(barNumber):
        b = get_height(barNumber)
        h = get_width(barNumber)
        Iwidth = (b*h**3)/12
        return(Iwidth)
    def inertiaHeight(barNumber):
        b = get_height(barNumber)
        h = get_width(barNumber)
        Iheight = (h*b**3)/12
        return(Iheight)

