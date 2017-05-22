// Give the dimensions of a subplot regarding the number of plot to draw
function m = GetSubPlotSize(n)
    x = int(n^0.5)
    y = ceil(n/x)
    m = [min(x,y),max(x,y)]
endfunction
