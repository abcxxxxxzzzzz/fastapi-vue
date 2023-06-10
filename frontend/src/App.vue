<template>
  <router-view></router-view>
</template>

<style>

#app {
  max-width: 100%;
  width: 100%;
  height: 100%;
  margin: 0 auto;
  padding: 0 0;
  text-align: center;
}

html, body {
  width: 100%;
  height: 100%;
  min-height: 100%;
  min-width: 100%;
}

#nprogress .bar {
  background-color: #f4f4f4 !important;
  height: 3px !important;
}



/* 鼠标下拉进度样式 */
::-webkit-scrollbar{
  width: 4px;
  height: 4px;
}

::-webkit-scrollbar-corner{
  display: block;
}

::-webkit-scrollbar-thumb{
  border-radius: 8px;
  background-color: rgba(0, 0, 0, 0.2);
}

::-webkit-scrollbar-thumb,
::-webkit-scrollbar-track{
  border-right-color: transparent;
  border-left-color: transparent;
  background-color: rgba(0, 0, 0, 0.1);
}


</style>
