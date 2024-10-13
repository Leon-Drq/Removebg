// import React, { useState, useRef } from 'react'
// import { Card, CardContent } from "./components/ui/card"
// import { Upload, Download } from 'lucide-react'
// import { toast } from "./components/ui/use-toast"
// import { Button } from "./components/ui/button";

// export default function BackgroundRemover() {
//   const [originalImage, setOriginalImage] = useState<string | null>(null)
//   const [processedImage, setProcessedImage] = useState<string | null>(null)
//   const [isProcessing, setIsProcessing] = useState(false)
//   const fileInputRef = useRef<HTMLInputElement>(null)

//   const handleImageUpload = (file: File) => {  // 修改：接收文件并上传
//     if (file && file.type.startsWith('image/')) {
//       const reader = new FileReader()
//       reader.onload = (e) => {
//         setOriginalImage(e.target?.result as string)
//         setProcessedImage(null) // Reset processed image when new image is uploaded
//       }
//       reader.readAsDataURL(file)
//       toast({
//         title: "图片上传成功",
//         description: "您可以点击'移除背景'按钮来处理图片。",
//       })
//     } else {
//       toast({
//         title: "上传失败",
//         description: "请上传有效的图片文件。",
//         variant: "destructive",
//       })
//     }
//   }

//   const triggerFileInput = () => {  // 修改：触发文件选择框
//     fileInputRef.current?.click()
//   }

//   const onDrop = (event: React.DragEvent<HTMLDivElement>) => {  // 新增：拖拽上传功能
//     event.preventDefault()
//     const file = event.dataTransfer.files?.[0]
//     if (file) {
//       handleImageUpload(file)
//     }
//   }

//   const removeBackground = async () => {
//     if (!originalImage) return

//     setIsProcessing(true)
//     try {
//       const response = await fetch('http://localhost:5000/remove-background', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ image: originalImage }),
//       })

//       if (!response.ok) {
//         throw new Error('Failed to process image')
//       }

//       const result = await response.json()
      
//       if (result.processedImage) {
//         setProcessedImage(result.processedImage)
//         toast({
//           title: "背景移除成功",
//           description: "您现在可以下载处理后的图片。",
//         })
//       } else {
//         throw new Error('Processed image not received')
//       }
//     } catch (error) {
//       console.error('Error processing image:', error)
//       toast({
//         title: "处理失败",
//         description: "移除背景时出现错误，请确保本地API服务正在运行并重试。",
//         variant: "destructive",
//       })
//     } finally {
//       setIsProcessing(false)
//     }
//   }

//   return (
//     <div className="container mx-auto p-4 h-screen">
//       <header className="flex items-center p-4 bg-white shadow-md mb-4">
//         <img src="/logo/my-logo.png" alt="Logo" className="h-12 w-12 mr-4" />
//         <h1 className="text-xl font-bold">Free BG remover: 最省事的在线抠图网站</h1>
//       </header>

//       <div className="flex flex-row h-full">
        
//         {/* Left side - Image upload and preview */}
//         <div className="w-1/2 pr-4">
//           <Card className="h-full">
//             <CardContent className="p-6 h-full flex flex-col">
//               <div 
//                 className="flex-grow aspect-square bg-muted relative flex items-center justify-center mb-4 border-dashed border-2 border-gray-400"
//                 onDrop={onDrop}  // 新增：处理拖拽事件
//                 onDragOver={(e) => e.preventDefault()}  // 新增：阻止默认行为以允许拖拽
//                 onClick={triggerFileInput}  // 修改：点击图标触发文件选择
//               >
//                 {originalImage ? (
//                   <img src={originalImage} alt="原图" className="max-w-full max-h-full object-contain" />
//                 ) : (
//                   <div className="text-center">
//                     <Upload className="mx-auto h-12 w-12 text-muted-foreground" />
//                     <p className="mt-2 text-sm text-muted-foreground">点击或拖拽图片上传</p> {/* 修改：更新提示 */}
//                   </div>
//                 )}
//               </div>
//               <input
//                 type="file"
//                 accept="image/*"
//                 onChange={(e) => e.target.files && handleImageUpload(e.target.files[0])}  // 修改：处理文件选择
//                 className="hidden"
//                 ref={fileInputRef}
//               />
//             </CardContent>
//           </Card>
//         </div>

//         {/* Right side - Controls and options */}
//         <div className="w-1/2 pl-4">
//           <Card className="h-full">
//             <CardContent className="p-6 h-full flex flex-col">
//               <Button
//                 onClick={removeBackground}
//                 disabled={!originalImage || isProcessing}
//                 className="w-full mb-6"
//               >
//                 {isProcessing ? '处理中...' : '移除背景'}
//               </Button>

//               {processedImage && (
//                 <div className="space-y-4 mb-6">
//                   <div className="aspect-square bg-muted relative flex items-center justify-center">
//                     <img src={processedImage} alt="处理后的图片" className="max-w-full max-h-full object-contain" />
//                   </div>
//                   <Button className="w-full flex items-center justify-center" onClick={() => {
//                     const link = document.createElement('a')
//                     link.href = processedImage
//                     link.download = 'processed-image.png'
//                     document.body.appendChild(link)
//                     link.click()
//                     document.body.removeChild(link)
//                   }}>
//                     <Download className="mr-2 h-4 w-4" /> 下载
//                   </Button>
//                   <div className="text-sm text-muted-foreground text-center">
//                     处理后的图片
//                   </div>
//                 </div>
//               )}
//             </CardContent>
//           </Card>
//         </div>
//       </div>
//     </div>
//   )
// }

import React, { useState, useRef } from 'react'
import { Card, CardContent } from "./components/ui/card"
import { Upload, Download } from 'lucide-react'
import { toast } from "./components/ui/use-toast"
import { Button } from "./components/ui/button";

export default function BackgroundRemover() {
  const [originalImage, setOriginalImage] = useState<string | null>(null)
  const [processedImage, setProcessedImage] = useState<string | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleImageUpload = (file: File) => {
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader()
      reader.onload = (e) => {
        setOriginalImage(e.target?.result as string)
        setProcessedImage(null)
      }
      reader.readAsDataURL(file)
      toast({
        title: "图片上传成功",
        description: "您可以点击'移除背景'按钮来处理图片。",
      })
    } else {
      toast({
        title: "上传失败",
        description: "请上传有效的图片文件。",
        variant: "destructive",
      })
    }
  }

  const triggerFileInput = () => {
    fileInputRef.current?.click()
  }

  const onDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    const file = event.dataTransfer.files?.[0]
    if (file) {
      handleImageUpload(file)
    }
  }

  const removeBackground = () => {
    if (!originalImage) return

    setIsProcessing(true)

    // 创建 WebSocket 连接
    const socket = new WebSocket("ws://localhost:5001")

    socket.onopen = () => {
      const request = {
        type: "remove_background",
        image: originalImage,
      }
      socket.send(JSON.stringify(request))
    }

    socket.onmessage = (event) => {
      const response = JSON.parse(event.data)

      if (response.type === "processed_image") {
        setProcessedImage(response.image)
        toast({
          title: "背景移除成功",
          description: "您现在可以下载处理后的图片。",
        })
      } else if (response.type === "error") {
        toast({
          title: "处理失败",
          description: response.message,
          variant: "destructive",
        })
      }
      setIsProcessing(false)
    }

    socket.onerror = (error) => {
      console.error('WebSocket Error:', error)
      toast({
        title: "连接失败",
        description: "无法连接到后台服务，请重试。",
        variant: "destructive",
      })
      setIsProcessing(false)
    }
  }

  return (
    <div className="container mx-auto p-4 h-screen">
      <header className="flex items-center p-4 bg-white shadow-md mb-4">
        <img src="/logo/my-logo.png" alt="Logo" className="h-12 w-12 mr-4" />
        <h1 className="text-xl font-bold">Free BG remover: 最方便的免费在线抠图网站</h1>
      </header>

      <div className="flex flex-row h-full">
        
        {/* 左侧 - 图片上传和预览 */}
        <div className="w-1/2 pr-4">
          <Card className="h-full">
            <CardContent className="p-6 h-full flex flex-col">
              <div 
                className="flex-grow aspect-square bg-muted relative flex items-center justify-center mb-4 border-dashed border-2 border-gray-400"
                onDrop={onDrop}
                onDragOver={(e) => e.preventDefault()}
                onClick={triggerFileInput}
              >
                {originalImage ? (
                  <img src={originalImage} alt="原图" className="max-w-full max-h-full object-contain" />
                ) : (
                  <div className="text-center">
                    <Upload className="mx-auto h-12 w-12 text-muted-foreground" />
                    <p className="mt-2 text-sm text-muted-foreground">点击或拖拽图片上传</p>
                  </div>
                )}
              </div>
              <input
                type="file"
                accept="image/*"
                onChange={(e) => e.target.files && handleImageUpload(e.target.files[0])}
                className="hidden"
                ref={fileInputRef}
              />
            </CardContent>
          </Card>
        </div>

        {/* 右侧 - 控制和选项 */}
        <div className="w-1/2 pl-4">
          <Card className="h-full">
            <CardContent className="p-6 h-full flex flex-col">
              <Button
                onClick={removeBackground}
                disabled={!originalImage || isProcessing}
                className="w-full mb-6"
              >
                {isProcessing ? '处理中...' : '移除背景'}
              </Button>

              {processedImage && (
                <div className="space-y-4 mb-6">
                  <div className="aspect-square bg-muted relative flex items-center justify-center">
                    <img src={processedImage} alt="处理后的图片" className="max-w-full max-h-full object-contain" />
                  </div>
                  <Button className="w-full flex items-center justify-center" onClick={() => {
                    const link = document.createElement('a')
                    link.href = processedImage
                    link.download = 'processed-image.png'
                    document.body.appendChild(link)
                    link.click()
                    document.body.removeChild(link)
                  }}>
                    <Download className="mr-2 h-4 w-4" /> 下载
                  </Button>
                  <div className="text-sm text-muted-foreground text-center">
                    处理后的图片
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
