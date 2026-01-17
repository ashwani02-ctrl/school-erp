"use client"
import { useEffect, useState } from "react"

export default function Page() {
  const [role, setRole] = useState("student");
  useEffect(() => {
    const fetchProfile = async () => {
      try{
        const res = await fetch("/api/profile", {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          }
        });
        
        if (!res.ok) throw Error("Profile fetch error")
        
        const result = await res.json();
        console.log("result.data: ", result.data);
        setRole(result.data.role);

      } catch (err) {
        console.log("Error: ", err);
      }
    }

    fetchProfile();
  })
  return (
    <>
    <section className="flex justify-center items-center h-screen">
    <p className="text-6xl font-bold"> Welcome to the <span className="capitalize text-center">{role}</span> Panel!</p>

    </section>
      
    </>
  )
}
