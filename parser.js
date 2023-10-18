function parseDomain(domainStr) {
    if (domainStr.includes("Reals")) {
      return "x כל";
    }
  
  const regexp = /Interval(?:\.open|\.Ropen|\.Lopen|\.Rclose|\.Lclose)?\((-oo|[\d\*\-pi\/]+|[\w\-]+\(.?\)),\s*(oo|[\d\*\-pi\/]+|[\w\-]+\(.?\))\)/g;
  
    let match;
    let intervals = [];
  
    while ((match = regexp.exec(domainStr)) !== null) {
      const type = match[0].substring(9, match[0].indexOf("(")); // Extract the type (e.g., .Ropen, .open)
      const startValue = match[1];
      const endValue = match[2];
  
      let intervalStr;
      switch (type) {
        case "open":
          intervalStr = `${startValue} < x < ${endValue}`;
          break;
        case "Ropen":
          intervalStr = `${startValue} <= x < ${endValue}`;
          break;
        case "Lopen":
          intervalStr = `${startValue} < x <= ${endValue}`;
          break;
        case "Rclose": // This will probably be reverse but kept for clarity
          intervalStr = `${startValue} < x <= ${endValue}`;
          break;
        case "Lclose": // This will probably be reverse but kept for clarity
          intervalStr = `${startValue} <= x < ${endValue}`;
          break;
        default:
          intervalStr = `${startValue} <= x <= ${endValue}`;
          break;
      }
      intervals.push(intervalStr);
    }
    
    return intervals.join(", ");
  }

  string1 = "Interval(log(5), log(4))"
  console.log(parseDomain(string1))