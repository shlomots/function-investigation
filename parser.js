function parseDomain(domainStr) {
    domainStr = domainStr.replace(/.open/g, "")
    domainStr = domainStr.replace(/.Ropen/g, "")
    domainStr = domainStr.replace(/.Lopen/g, "")
    domainStr = domainStr.replace(/.close/g, "")
    domainStr = domainStr.replace(/.Rclose/g, "")
    domainStr = domainStr.replace(/.Lclose/g, "")
    if (domainStr.includes("Reals")) {
        return "all x";
    } 
    else if (domainStr.includes("Union(")) {
        domainStr = domainStr.replace("Union(", "");      // Remove the "Union(" prefix
        domainStr = domainStr.slice(0, -1);   
        intervals = domainStr.split("),")// slice(1) to skip the initial empty string before the first "Union"
        const formattedIntervals = intervals.map(interval => {
             return interval.replace("Interval(", "").replace("Interval.(", "").replace(")", "").replace(",", " < x < ");
        });
        return formattedIntervals.join(", ").replace(")","");            // Remove the trailing ")"
    }
    else {
        intervals = domainStr.split("),")// slice(1) to skip the initial empty string before the first "Union"
        const formattedIntervals = intervals.map(interval => {
             return interval.replace("Interval(", "").replace(")", "").replace(",", " < x < ");
        });
        return formattedIntervals.join(", ").replace(")","");
    }
}

function parseDomain2(domainStr) {
    // Regular expression to capture numbers, oo, or -oo
    const numberOrInfinity = /(-?oo|-?\d+)/;

    // Replace Interval.open(a,b) to a < x < b
    domainStr = domainStr.replace(/Interval\.open\((-?oo|-?\d+),(-?oo|-?\d+)\)/g, '$1 < x < $2');

    // Replace Interval.Ropen(a,b) to a < x <= b
    domainStr = domainStr.replace(/Interval\.Ropen\((-?oo|-?\d+),(-?oo|-?\d+)\)/g, '$1 < x <= $2');

    // Replace Interval.Lopen(a,b) to a <= x < b
    domainStr = domainStr.replace(/Interval\.Lopen\((-?oo|-?\d+),(-?oo|-?\d+)\)/g, '$1 <= x < $2');

    // Replace Interval(a,b) to a <= x <= b
    domainStr = domainStr.replace(/Interval\((-?oo|-?\d+),(-?oo|-?\d+)\)/g, '$1 <= x <= $2');
    
    return domainStr;
}


function parseIncreasingDecreasing(intervals) {
    if (!Array.isArray(intervals)) {
        console.error("Expected an array, but received:", intervals);
        return '';
    }

    const formattedIntervals = intervals.map(intervalStr => {
        // Split the string to get the interval values
        const interval = intervalStr.replace(/[\[\]]/g, '').split(',');

        if (interval && interval.length === 2) {
            let start = (interval[0] === "oo" ? "∞" : (interval[0] === "-oo" ? "-∞" : interval[0]));
            let end = (interval[1] === "oo" ? "∞" : (interval[1] === "-oo" ? "-∞" : interval[1]));
            return `${start} < x < ${end}`;
        } else {
            console.error("Unexpected interval format:", intervalStr);
            return '';  // or some default string representation
        }
    });
    
    return formattedIntervals.join(", ");
}



// const domain = "Union(Interval.Ropen(-2*pi, -3*pi/2), Interval.open(-3*pi/2, -pi/2), Interval.open(-pi/2, pi/2), Interval.open(pi/2, 3*pi/2), Interval.Lopen(3*pi/2, 2*pi))"; // Replace with your actual input
// const parsedDomain = parseDomain2(domain);
// console.log(parsedDomain);
// const domainStr = "Union(Interval(-oo, 2), Interval(3, oo))";
// const regex = /Interval\((-oo|\d+),\s*(-oo|\d+)\)/g;

// for (const match of domainStr.matchAll(regex)) {
//     console.log("Start of interval:", match[1]);
//     console.log("End of interval:", match[2]);
// }
const regexp = /Interval(?:\.open|\.Ropen|\.Lopen|\.Rclose|\.Lclose)?\((-oo|\d+),\s*(oo|\d+)\)/g;
const str = "Interval(3, 2)";
let match;

while ((match = regexp.exec(str)) !== null) {
    const type = match[0].substring(9, match[0].indexOf("(")); // Extract the type (e.g., .Ropen, .open)
    const startValue = match[1];
    const endValue = match[2];

    let formattedInterval;
    switch (type) {
        case "open":
            formattedInterval = `${startValue} < x < ${endValue}`;
            break;
        case "Ropen":
            formattedInterval = `${startValue} <= x < ${endValue}`;
            break;
        case "Lopen":
            formattedInterval = `${startValue} < x <= ${endValue}`;
            break;
        case "Rclose": // This will probably be reverse but kept for clarity
            formattedInterval = `${startValue} < x <= ${endValue}`;
            break;
        case "Lclose": // This will probably be reverse but kept for clarity
            formattedInterval = `${startValue} <= x < ${endValue}`;
            break;
        default:
            formattedInterval = `${startValue} <= x <= ${endValue}`;
            break;
    }
    console.log(formattedInterval);
}