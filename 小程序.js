Page({

    /**
     * 页面的初始数据
     */
    data: {
      isConnect: null,
      text1:"0/1200",
      text2:"0min"
    },
    startClick(even) {
      wx.connectSocket({
        url: 'ws://192.168.3.3:8001/',
        method: 'GET',
        success: (res) => {
          isConnect: true
          console.log("连接成功", res)
        },
        fail: (res) => {
          isConnect: false
          console.log("连接失败", res)
        }
      });
  
      wx.onSocketOpen((res) => {
        console.log('WebSocket连接已打开！')
      });
  
      wx.onSocketError((res) => {
        console.log('WebSocket连接打开失败，请检查！')
      })
    },
  
    getClick1: function (even) {
      wx.sendSocketMessage({
        data: "getpersons"
      }
      )
      var newthis=this
      wx.onSocketMessage(function(data) {
         newthis.setData({
          text1:data.data
        })
      })
  
    },
    getClick2: function (even) {
      wx.sendSocketMessage({
        data: "gettime"
      }
      )
      var newthis=this
      wx.onSocketMessage(function(data) {
         newthis.setData({
          text2:data.data
        })
      })
  
    },
    closeClick(even) {
      wx.closeSocket({
        success: (res) => {
          console.log("关闭成功...")
        },
        fail: (res) => {
          console.log("关闭失败...")
        }
      });
      wx.onSocketClose((res)=>  {
        console.log("WebSocket连接已关闭")
      })
    },
  
    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {
      wx.onSocketMessage((res) => {
        console.log(res.data)
        console.log(res)
      })
    }
  })