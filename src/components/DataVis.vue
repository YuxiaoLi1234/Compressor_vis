<template>
    <div id="data_vis">
        
        <svg id="data_svg">

        </svg>
        <t-space  size="40px">
        <t-slider id ='slider' v-model="value1" :show-tooltip="true" :inputNumberProps="inputNumberProps" v-on:change="update"/>
        </t-space>

        <!-- color -->
        <t-space id='color' size="5px">
        <t-space direction="vertical" size="5px" class="item">
            <h5>min</h5>
            <t-color-picker v-model="color1" format="HEX" :color-modes="['monochrome']" v-on:change="update"/>
        </t-space>
        <t-space direction="vertical" size="5px" class="item">
            <h5>max</h5>
            <t-color-picker v-model="color2" format="HEX" :color-modes="['monochrome']" v-on:change="update"/>
        </t-space>
        </t-space>

    </div>
</template>

<script>
import * as d3 from 'd3'
import parameters from '../../js/get_data.js';
export default {
  name:'DataVis',
  data(){
      return{
          parameters:parameters,
          input_data:'',
          value1: 23,
          inputNumberProps: { theme: 'column'},
          svg:'',
          margin:40,
          width:(window.innerWidth*0.28)/1.05,
          height:(window.innerHeight)*0.7/1.05,
          color1: '#FFA500',
          color2: '#006400',
          rects:null,
      };
  },
  mounted(){
    this.data_vis()
  },
  methods:{
    data_vis:function(){

        
        
        this.svg = d3.select("#data_svg")
                .attr("width", this.width )
                .attr("height", this.height)
                
        d3.json('./data/inputdata.json').then((d)=>{
            this.input_data = d
            document.getElementById('slider').max=d.length-1
            this.draw_slice(d[23])
            
            
        })

        
        
    },
    draw_slice:function(data){

        let group = this.svg.append("g");
        let newArray = data.flat(Infinity)
        const this_min = Math.min(...newArray)
        const this_max = Math.max(...newArray)
        const number = data.length
        // console.log(data.length)
        // console.log(this_min,this_max)
        // const scale_x = d3.scaleLinear().domain([0,data.length]).range([0.5*margin,width-0.5*margin])
        // const scale_y = d3.scaleLinear().domain([0,data[0].length]).range([width-0.5*margin,0.5*margin])
        let colorscale = d3.scaleLinear().domain([this_min,this_max]).range(['#FFA500','#006400'])
        // draw each slice first
        // for(let j =0;j<data.length;j++){
        this.rects = group
                    .append("g")
                    .selectAll() // make path 
                    .data(newArray)
                    .enter()
                    
                    .append("rect")
                    .attr('class','rects')
                    .attr('x',(d,i)=>this.margin+(i % number)*.86)
                    .attr('y',(d,i)=>this.margin+(parseInt(i / number)*.86))
                    .attr('fill',d=>colorscale(d))
                    .attr('width',.4)
                    .attr('height',.4)
                    .attr('opacity',.95)
        // }

        },
    update:function(){
        // console.log(this.color1)
        const data = this.input_data[this.value1].flat(Infinity)
        const this_min = Math.min(...data)
        const this_max = Math.max(...data)
        let colorscale = d3.scaleLinear().domain([this_min,this_max]).range([this.color1,this.color2])
        
        this.rects.style("fill",(d,i)=>colorscale(data[i]))
    }

  }
}
</script>

<style scoped>
#data_vis{
    border:2px solid #a7b2ac;
    border-radius: 4px;
    position:absolute;
    top:28%;
    left:.7%;
    width: 28%;
    height: 70%;
}
#data_svg{
    position: absolute;
    top:10%;
    left:-2%
}
#slider{
    position: absolute;
    top:92%;
    left:10%;
    width:88%
}

#color{
    position: absolute;
    top:-1%;
    left:10%;
}
.item h5 {
  font-weight: normal;
}
</style>