<template>
    <!-- <div id="chart" style="height:100%;width:100%"></div> -->
    <t-button id="compressor" v-on:click="update">compressor_selection</t-button>
    <div id="stat">
        
    </div>

</template>
  
  <script>
  import * as d3 from 'd3' 
  import * as echarts from 'echarts'
import parameters from '../../js/get_data.js'
  export default {
    name:'StatA',
    data(){
        return{
            parameters:parameters,
            svg:'',
            option:{
                angleAxis: {
                    type: 'category',
                    data: ''
                },
                radiusAxis: {},
                polar: {},
                
                series: '',
                legend: {
                    show: true,
                    data: ''
                }
            },
            myChart:''
        }
        
        
    },
    mounted() {
        
        // this.get_data()
        
        setTimeout(()=>{
            this.draw_levels()
            // this.draw_parallel_c(this.parameters)
        },1000)
        
    },
    computed: {
    },
    methods:{
       
        draw_levels:function(){
            
            const parameters = this.parameters
            const name = Array.from(new Set(parameters.map(item=>item['compressor_id'])))
            
            this.option.angleAxis.data = parameters.map(item=>Object.keys(item))[0].filter(d=>d!='compressor_id').map(d=>d.split(':')[1])
            let series = []
            // console.log(Object.values(parameters[0]).filter((item,i)=>Object.keys(parameters[0])[i]!='compressor_id'))
            this.option.legend.data=name
            name.forEach((item,i)=>{
                // console.log(Object.values(parameters[0]).filter((item,j)=>Object.keys(parameters[0])[j]!='compressor_id'))
                let obj = 
                    {
                    type: 'bar',
                    data: Object.values(parameters[i]).filter((item,j)=>Object.keys(parameters[i])[j]!='compressor_id'),
                    coordinateSystem: 'polar',
                    name: item,
                    stack: 'a',
                    emphasis: {
                        focus: 'series'
                    }
                    }
                series.push(obj)
            })
            this.option.series = series
            const that = this
            let width = (window.innerWidth*0.7)/1.05;
            let height = (window.innerHeight)*0.6/1.05;
            
            
            var chartDom = document.getElementById('stat');
            that.myChart = echarts.init(chartDom);
            var option = that.option
            option && that.myChart.setOption(option);
            that.myChart.on("click",function(params){
                that.myChart.dispose()
                that.myChart = null
                console.log(params.seriesName,that.myChart)
                that.svg = d3.select("#stat").append('svg').attr('id','SVG')
                .attr("width", width )
                .attr("height", height*1.2);
                that.draw_parallel_c(that.parameters)
            })
            
            
        },
        draw_parallel_c: function(data1){
            
            const svg = this.svg
            let width = (window.innerWidth*0.7)/1.05;
            let height = (window.innerHeight)*0.6/1.05;
            let margin = 40;
            // console.log(document.getElementById('stat').clientHeight)

            let species = ['sz','zfp'];
            let group = svg.append("g");
            let legend = svg.append("g");

            let dimensions = data1.columns.slice(1);
            
            
            // console.log(data.map(d=>d['compressor_id']))
            // build colorscale
            let colorScale = d3.scaleOrdinal()
                .domain(['sz','zfp'])
                .range(['#6495ED', '#FFB6C1']);

            // build xaxis to help make yaxis
            let scaleX = d3.scalePoint()
                .domain(dimensions)
                .range([0, width - 0.5*margin]);

            // build yscale for every dimension.
            let scaleY = {}
            
            dimensions.forEach(function (d) {
                // console.log(data1.map(e => eval(e[d])))
                scaleY[d] = d3.scaleLinear()
                    .domain([d3.min(data1.map(e => eval(e[d]))), d3.max(data1.map(e => eval(e[d])))])
                    .range([height-0.5*margin,0])
            });

            // build a path generator
            let lineGenerator = d3.line();

            // draw the line
            group
                .append("g")
                .selectAll() // make path 
                .data(data1)
                .enter()
                .append("path")
                .attr("d", d => lineGenerator(  
                    dimensions.map(function (p) { 
                        return [scaleX(p), scaleY[p](d[p])];
                    })
                ))
                .attr("fill", "none")
                .attr("class", d => d['compressor_id']) // bound class
                .attr("stroke", d => colorScale(d['compressor_id']))
                .attr("stroke-width", 2)
                .attr("opacity",1)
                .on("mouseover", function () { // hightlight
                    d3.select(this).attr('stroke-width', 5).attr('opacity', 1)
                })
                .on("mouseout", function () { 
                    d3.select(this).transition().attr('stroke-width', 1.5).attr('opacity', .5)
                });
            
            let Ys = group
                .selectAll(".dimension")
                .data(dimensions)
                .enter()
                .append('g')
                .attr("class", '1')
                .attr("transform", d => `translate(${scaleX(d)},0)`);
            console.log(group)
            
            
            Ys.append("g")
                .each(function (d) {
                    d3.select(this).call(d3.axisLeft(scaleY[d]).ticks(5).tickFormat(d=>eval(d).toExponential()))
            });

            
            Ys.append("text")
                .attr("x", -0.05 * width) 
                .attr("y", -0.05 * height)
                .attr('font-size', 10)
                .text(d => { 
                    return d.split(':').length==1?d.split(':')[0]:d.split(':')[1]});

            
            Ys.selectAll("text")
                .clone(true)
                .lower()
                .attr("fill", "none")
                .attr("stroke-width", 5)
                .attr("stroke-linejoin", "round")
                .attr("stroke", "white");

            
            group.attr("transform", `translate(100, 80)`);


            // ******************** legend ********************

            let flag = { 'sz': true, 'zfp': true };

            
            // 
            // console.log(species[0])
            legend.selectAll(".circles")
                .data(species)
                .enter()
                .append("circle")
                .attr("fill", d => colorScale(d))
                .attr('cx', 10)
                .attr('cy', (d, i) => i * 25 + 30)
                .attr('r', 8)
                .on("mouseover", function () { // 突出显示鼠标滑过的图标
                    d3.select(this).transition().attr('r', 12)
                })
                .on("mouseout", function () { // 还原
                    d3.select(this).transition().attr('r', 8)
                })
                .on("click", function (event, d) { 
                    // console.log(d)
                    // console.log(d3.select(this))// 
                    if (flag[d]) { // 
                        d3.select(this).attr('fill', 'lightgrey') // 
                        d3.selectAll(`.${d}`).attr('stroke', 'lightgrey') // 
                        flag[d] = !flag[d] // 
                    }
                    else { // 
                        d3.select(this).attr('fill', e => colorScale(e))
                        d3.selectAll(`.${d}`).attr('stroke', e => colorScale(e['compressor_id']))
                        flag[d] = !flag[d]
                    }
                });

            // 
            legend.selectAll(".texts")
                .data(species)
                .enter()
                .append("text")
                .attr('x', 30)
                .attr('y', (d, i) => i * 25 + 35)
                .text(d => d);

            // 
            legend.attr('transform', `translate(5,20)`);
        },
        update:function(){
            d3.select('#SVG').remove()
            this.draw_levels()
        }

    },
  
  }
  </script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style scoped>
  #stat{
      border:2px solid #a7b2ac;
      border-radius: 4px;
      position:absolute;
      top:28%;
      left:29.3%;
      width: 70%;
      height: 70%;
};
#chart{
    position:absolute;
    top:28%;
    left:29.3%;
    width: 70%;
    height: 70%;
}


/* #data_selection{
    border:2px solid #a7b2ac;
    border-radius: 4px;
    position:absolute;
    top:1%;
    left:.7%;
    width: 28%;
    height: 26%;
}

#parameter{
    border:2px solid #a7b2ac;
    border-radius: 4px;
    position:absolute;
    top:1%;
    left:29.3%;
    width: 70%;
    height: 26%;
}

#data_vis{
    border:2px solid #a7b2ac;
    border-radius: 4px;
    position:absolute;
    top:28%;
    left:.7%;
    width: 28%;
    height: 70%;
} */
#compressor{
    z-index:101;
    position:absolute;
    top:30%;
    left:80%;
    
}
  </style>

