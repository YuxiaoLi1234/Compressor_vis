<template>
    <div id="data_selection">
        <p>Enter your Configuration here</p>
        <t-input id = 'input1' v-model="compressor_id" placeholder='null' label="compressor_id:"  @enter="update"/>
        <t-input id = 'input2' v-model="early_config" placeholder='null' label="early_config:"  @enter="update"/>
        <t-input id = 'input3' v-model="compressor_config" placeholder='null' label="compressor_config:"  @enter="update"/>
    </div>
    <!-- need a place to upload the inputdata -->
</template>

<script>
import axios from 'axios'

export default {
  name:'DataSelection',
  data(){
      return{
        compressor_id:'',
        early_config:'',
        compressor_config:'',
        msg:''
      };
  },
  methods:{
    update:function(){
        console.log('changed')
        if(this.compressor_id.length == 0 || this.early_config.length == 0 || this.compressor_config.length == 0){
            this.msg = this.$message.info({
                    content: 'input is illegal',
                    theme:"warning",
                    duration: 1000,
                    // 层级控制：非当前场景自由控制开关的关键代码，仅用于测试 API 是否运行正常
                    zIndex: 1001,
                    // 挂载元素控制：非当前场景自由控制开关的关键代码，仅用于测试 API 是否运行正常
                    attach: document.body,
                });
        }
        else{
            axios.post('http://localhost:5000/indexlist',{
            'compressor_id':this.compressor_id,
            'early_config':this.early_config,
            'compressor_config':this.compressor_config
            }).then(response=>{
                // let need1 = eval('('+response.data['configration']+')')
                console.log(response.data)
            })
            .catch((error)=>{
                console.log(error)
            })
        }
        
    }
  }
}
</script>

<style scoped>
#data_selection{
    border:2px solid #a7b2ac;
    border-radius: 4px;
    position:absolute;
    top:1%;
    left:.7%;
    width: 28%;
    height: 26%;
}
#input1{
    position:absolute;
    width:70%;
    top:25%;
    left:10%
}
#input2{
    position:absolute;
    width:70%;
    top:45%;
    left:10%
}
#input3{
    position:absolute;
    width:70%;
    top:65%;
    left:10%
}
p{
    position:absolute;
    left:10%
}
</style>