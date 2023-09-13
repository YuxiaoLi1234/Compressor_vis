import * as d3 from 'd3'
let parameters
async function data() {
    return d3.csv("./data/result.csv").then((d)=>{
        parameters = d
    })
  }
await data()
console.log('d',parameters)
// setTimeout(() => {
//     console.log(parameters)
    
// }, 1000)

export default parameters