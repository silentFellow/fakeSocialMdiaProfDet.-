import React from 'react'
import { useState } from 'react'
import axios from 'axios'

const Home = () => {

  const [uname, setUname] = useState('')
  const [loading, setLoading] = useState(false)
  const [resAvail, setResAvail] = useState(false)
  const [followers, setFollowers] = useState('')
  const [following, setFollowing] = useState('')
  const [posts, setPosts] = useState('')
  const [check, setCheck] = useState('')

  const run = async () => {
    setLoading(true)
    try {
      const res = await axios.get('http://127.0.0.1:8000/checkProf/' + uname)
      setResAvail(true)
      console.log(res)
      setFollowers(res.data.followers)
      setFollowing(res.data.following)
      setPosts(res.data.posts)
      setCheck(res.data.check)
    }
    catch(e) {
      console.log(e)
    }
    finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-full w-[50%] fixed bg-lprimary flex-col">
      <div className="h-[10%] w-full flex justify-center items-center bg-white font-pacifico text-[24px]">FakesNoMore.com</div>
      <div className="flex flex-col justify-center items-center h-full w-full">
        <input type="text" className="h-[6%] w-[80%] px-2 pl-6 text-lsecondary outline outline-lascent outline-1" placeholder='Enter a valid username' onChange={(e) => setUname(e.target.value)} />
        <button className="p-3 bg-lsecondary text-lprimary mt-6 rounded-lg" onClick={() => run()}>Submit</button>

        <div className={`${loading ? "w-[60%] flex justify-center items-center bg-lsecondary p-3 rounded-md mt-4 text-lprimary" : 'hidden'}`}>
          Please wait, while processing...
        </div>

        <div className={`${resAvail ? "h-[42%] w-[80%] p-[30px] bg-red-700 mt-[30px] rounded-md flex flex-col justify-center items-center" : 'hidden'}`}>

          <div className="h-[80%] w-full flex">
            <div className="h-full w-[48%] flex flex-col justify-center items-center">
              <h1 className="w-full text-lprimary my-4 text-[18px] font-poppins">Username </h1>
              <h1 className="w-full text-lprimary my-4 text-[18px] font-poppins">Followers </h1>
              <h1 className="w-full text-lprimary my-4 text-[18px] font-poppins">Following </h1>
              <h1 className="w-full text-lprimary my-4 text-[18px] font-poppins">Posts</h1>
            </div>
            <div className="h-full w-[2%] flex flex-col justify-center items-center">
              <h1 className="w-full text-lprimary my-4 text-[18px] font-poppins"> : </h1>
              <h1 className="w-full text-lprimary my-4 text-[18px] font-poppins"> : </h1>
              <h1 className="w-full text-lprimary my-4 text-[18px] font-poppins"> : </h1>
              <h1 className="w-full text-lprimary my-4 text-[18px] font-poppins"> : </h1>
            </div>
            <div className="h-full w-[48%] flex flex-col justify-center items-center ml-9">
              <h1 className="w-full text-lascent my-4 text-[18px] font-poppins">{uname}</h1>
              <h1 className="w-full text-lascent my-4 text-[18px] font-poppins">{followers}</h1>
              <h1 className="w-full text-lascent my-4 text-[18px] font-poppins">{following}</h1>
              <h1 className="w-full text-lascent my-4 text-[18px] font-poppins">{posts}</h1>
            </div>
          </div>

          <div className="h-[20%] w-full p-3 flex justify-center items-center bg-lprimary mt-[18px] rounded-xl">
            <span className="text-lascent font-[30px]">The profile is {check}.</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home