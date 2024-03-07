"use client";
import { PaperClipIcon } from "@heroicons/react/20/solid";
import React, { useEffect, useState } from "react";
import useVerify from "@/services/auth/auth";

export default function Account() {
  const { verify } = useVerify();
  useEffect(() => {
    verify();
    setName(localStorage.getItem("name"));
    setSurname(localStorage.getItem("surname"));
    setUsername(localStorage.getItem("username"));
  }, [verify]);

  const [name, setName] = useState("");
  const [username, setUsername] = useState("");
  const [surname, setSurname] = useState("");

  return (
    <div className=" flex flex-col justify-center items-center">
      <div className="px-4 sm:px-0 mt-20">
        <h3 className="text-base font-semibold leading-7 text-gray-900">
          Applicant Information
        </h3>
        <p className="mt-1 max-w-2xl text-sm leading-6 text-gray-500">
          Personal details and application.
        </p>
      </div>
      <div className="mt-6 border-t border-gray-100 mx-auto w-[80%]">
        <dl className="divide-y divide-gray-100">
          <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm font-medium leading-6 text-gray-900">
              Full name
            </dt>
            <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
              {`${name} ${surname}`}
            </dd>
          </div>
          <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm font-medium leading-6 text-gray-900">
              Username
            </dt>
            <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
              {`${username}`}
            </dd>
          </div>
        </dl>
      </div>
    </div>
  );
}
