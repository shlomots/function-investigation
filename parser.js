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
const domain = "Union(Interval.Ropen(-2*pi, -3*pi/2), Interval.open(-3*pi/2, -pi/2), Interval.open(-pi/2, pi/2), Interval.open(pi/2, 3*pi/2), Interval.Lopen(3*pi/2, 2*pi))"; // Replace with your actual input
const parsedDomain = parseDomain(domain);
console.log(parsedDomain);
