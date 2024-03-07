"use client";
import React, { useState, useEffect } from "react";
import { CheckIcon } from "@heroicons/react/24/outline";
import {
  useFetchIHAsQuery,
  useAddReservationMutation,
} from "@/services/apis/users_api";
import useVerify from "@/services/auth/auth";

export default function Iha() {
  const { verify } = useVerify();
  useEffect(() => {
    verify();
  }, [verify]);
  const { data: iha, isLoading, isError } = useFetchIHAsQuery();
  const [addReservation] = useAddReservationMutation();

  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [number, setNumber] = useState(1);
  const [loading, setLoading] = useState(false);

  function convertToCustomFormat(isoDateString) {
    const date = new Date(isoDateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    const seconds = String(date.getSeconds()).padStart(2, "0");
    const milliseconds = String(date.getMilliseconds()).padStart(3, "0");

    const customFormat = `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;

    return customFormat;
  }

  const handleRent = async (data_iha) => {
    try {
      setLoading(true);

      const response = await addReservation({
        iha_id: data_iha.id,
        customer_id: localStorage.getItem("id"),
        start_date: convertToCustomFormat(startDate),
        finish_date: convertToCustomFormat(endDate),
        number: number,
      }).unwrap();

      setLoading(false);
    } catch (error) {
      console.error(error);

      setLoading(false);
    }
  };

  return (
    <>
      <div className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
        <ul role="list" className="divide-y divide-gray-100">
          {isLoading
            ? "loading"
            : iha?.data?.map((data_iha) => (
                <li
                  key={data_iha.model}
                  className="flex justify-between gap-x-6 py-5"
                >
                  <div className="flex min-w-0 gap-x-4">
                    <img
                      className="h-24 w-24 flex-none bg-gray-50 object-contain"
                      src={
                        data_iha.image_url
                          ? `http://127.0.0.1:8000/${data_iha.image_url}`
                          : "https://lh3.googleusercontent.com/proxy/93IoZkVT12ZWW8IAH98bTFP2_jfxI7BjBRDzBLLKfefZpOqL_r4HaHa_NtM7LWv2WP4gtlu5utHVhW1dQGvue_S5xQNvidU"
                      }
                      alt=""
                    />
                    <div className="min-w-0 flex-auto">
                      <p className="text-sm font-semibold leading-6 text-gray-900">
                        {`${data_iha.brand} ${data_iha.model}`}
                      </p>
                      <p className="mt-1 truncate text-xs leading-5 text-gray-500">
                        {`Category: ${data_iha.category}`}
                      </p>
                      <p className="mt-1 truncate text-xs leading-5 text-gray-500">
                        {`Weight: ${data_iha.weight}`}
                      </p>
                      <p className="mt-1 truncate text-xs leading-5 text-gray-500">
                        {`Price: ${data_iha.price}/Hour`}
                      </p>
                    </div>
                  </div>

                  <div className="flex flex-col">
                    <label
                      htmlFor="start-date"
                      className="block text-sm font-medium leading-6 text-gray-900"
                    >
                      Start Date
                    </label>
                    <input
                      type="datetime-local"
                      id="start-date"
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      value={startDate}
                      onChange={(e) => setStartDate(e.target.value)}
                    />

                    <label
                      htmlFor="end-date"
                      className="block text-sm font-medium leading-6 text-gray-900 mt-4"
                    >
                      Finish Date
                    </label>
                    <input
                      type="datetime-local"
                      id="end-date"
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      value={endDate}
                      onChange={(e) => setEndDate(e.target.value)}
                    />
                    <label
                      htmlFor="end-date"
                      className="block text-sm font-medium leading-6 text-gray-900 mt-4"
                    >
                      Number
                    </label>
                    <input
                      type="number"
                      id="end-date"
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      value={number}
                      onChange={(e) => setNumber(e.target.value)}
                    />

                    <button
                      type="button"
                      className="mt-4 inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      onClick={() => handleRent(data_iha)}
                    >
                      {loading ? (
                        "loading"
                      ) : (
                        <>
                          <CheckIcon
                            className="-ml-0.5 mr-2 h-5 w-5"
                            aria-hidden="true"
                          />
                          Rent
                        </>
                      )}
                    </button>
                  </div>
                </li>
              ))}
        </ul>
      </div>
    </>
  );
}
