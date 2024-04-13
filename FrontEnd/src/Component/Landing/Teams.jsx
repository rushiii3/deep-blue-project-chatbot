import React from 'react'

const Teams = () => {
    const info = [
        {
            "name":"Hrushikesh Shinde",
            "image":"https://res.cloudinary.com/dmuhioahv/image/upload/v1694342370/IMG_9440.jpg",
            "job":"Website"
        },
        {
            "name":"Aaditya Pal",
            "image":"https://res.cloudinary.com/dmuhioahv/image/upload/v1706454922/WhatsApp_Image_2024-01-28_at_8.42.46_PM_txczyy.jpg",
            "job":"PDF extration"
        },
        {
            "name":"Aryan Bagwe",
            "image":"https://res.cloudinary.com/dmuhioahv/image/upload/v1706454922/WhatsApp_Image_2024-01-28_at_3.41.23_PM_e3c0zc.jpg",
            "job":"FAQ Generation"
        },
        {
            "name":"Pratik Kumbhar",
            "image":"https://res.cloudinary.com/dmuhioahv/image/upload/v1694934518/vulsoo6xmgaxpwxbjjez.jpg",
            "job":"Data Intents"
        }
    ]
  return (
    <div class="flex items-center justify-center w-full px-8 py-10 border-t border-gray-200 md:py-16 lg:py-24 xl:py-40 xl:px-0">
        <div class="flex flex-col">
    
            <div class="flex flex-col mt-8">
                <div class="container max-w-7xl px-4">
                    <div class="flex flex-wrap justify-center text-center mb-24">
                        <div class="w-full lg:w-6/12 px-4">
                            <h1 class="text-gray-900 text-4xl font-bold mb-8">
                                Meet the Team
                            </h1>
    
                            <p class="text-gray-700 text-lg font-light">
                                With over 100 years of combined experience, we've got a well-seasoned team at the helm.
                            </p>
                        </div>
                    </div>
    
                    <div class="flex flex-wrap">
                        {
                            info.map((value,key)=>(
                                <div class="w-full md:w-6/12 lg:w-3/12 mb-6 px-6 sm:px-6 lg:px-4" key={key}>
                                <div class="flex flex-col">
                                    <a href="#" class="mx-auto">
                                        <img class="rounded-2xl drop-shadow-md hover:drop-shadow-xl transition-all duration-200 delay-100 h-96"
                                            src={value.image} />
                                    </a>
        
                                    <div class="text-center mt-6">
                                        <h1 class="text-gray-900 text-xl font-bold mb-1">
                                            {value.name}
                                        </h1>
        
                                        <div class="text-gray-700 font-light mb-2">
                                            {value.job}
                                        </div>
        
                                        <div class="flex items-center justify-center opacity-50 hover:opacity-100
                                        transition-opacity duration-300">
                                            <a href="#" class="flex rounded-full hover:bg-indigo-50 h-10 w-10">
                                                <i class="mdi mdi-linkedin text-indigo-500 mx-auto mt-2"></i>
                                            </a>
        
                                            <a href="#" class="flex rounded-full hover:bg-blue-50 h-10 w-10">
                                                <i class="mdi mdi-twitter text-blue-300 mx-auto mt-2"></i>
                                            </a>
        
                                            <a href="#" class="flex rounded-full hover:bg-orange-50 h-10 w-10">
                                                <i class="mdi mdi-instagram text-orange-400 mx-auto mt-2"></i>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            ))
                        }
                    </div>
                </div>
            </div>
        </div>
    </div>
  )
}

export default Teams