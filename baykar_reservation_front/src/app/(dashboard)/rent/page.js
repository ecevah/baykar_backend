"use client";
import {
  useFetchReservationsQuery,
  useRemoveReservationMutation,
} from "@/services/apis/users_api";
import React, { useEffect, useState } from "react";
import useVerify from "@/services/auth/auth";

export default function Reservations() {
  const { verify } = useVerify();
  useEffect(() => {
    verify();
  }, [verify]);
  const [loading, setLoading] = useState(false);
  const {
    data: reservations,
    isLoading,
    isError,
    refetch, // Eklediğimiz refetch fonksiyonu
  } = useFetchReservationsQuery();

  const [removeReservation] = useRemoveReservationMutation();

  const handleDelete = async (reservationId) => {
    console.log(reservationId);
    try {
      setLoading(true);
      const response = await removeReservation(reservationId);

      if (response.error) {
        throw new Error(`Failed to delete reservation: ${response.error}`);
      }

      console.log("Reservation deleted successfully!");
      setLoading(false);
      // Silme işlemi tamamlandıktan sonra verileri yeniden getir
      refetch();
    } catch (error) {
      console.error("Error deleting reservation:", error);
      setLoading(false);
    }
  };

  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error fetching data</div>;

  function convertToCustomFormat(isoDateString) {
    const date = new Date(isoDateString);

    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();

    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");

    const customFormat = `${day}.${month}.${year} ${hours}:${minutes}`;

    return customFormat;
  }
  return (
    <>
      <div className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
        <ul role="list" className="divide-y divide-gray-100">
          {isLoading
            ? "loading"
            : reservations.data.map((reservation) => (
                <li
                  key={reservation.model}
                  className="flex justify-between gap-x-6 py-5"
                  onClick={() => null}
                >
                  <div className="flex min-w-0 gap-x-4">
                    <img
                      className="h-24 w-24 flex-none bg-gray-50 object-contain"
                      src={
                        reservation.iha.image_url
                          ? `http://127.0.0.1:8000/${reservation.iha.image_url}`
                          : "https://lh3.googleusercontent.com/proxy/93IoZkVT12ZWW8IAH98bTFP2_jfxI7BjBRDzBLLKfefZpOqL_r4HaHa_NtM7LWv2WP4gtlu5utHVhW1dQGvue_S5xQNvidU"
                      }
                      alt=""
                    />
                    <div className="min-w-0 flex-auto">
                      <p className="text-sm font-semibold leading-6 text-gray-900">
                        {`${reservation.iha.brand} ${reservation.iha.model}`}
                      </p>
                      <p className="mt-1 truncate text-xs leading-5 text-gray-500">
                        {`Category: ${reservation.iha.category}`}
                      </p>
                      <p className="mt-1 truncate text-xs leading-5 text-gray-500">
                        {`Weight: ${reservation.iha.weight}`}
                      </p>
                      <p className="mt-1 truncate text-xs leading-5 text-gray-500">
                        {`Price: ${reservation.iha.price} TL / Hour`}
                      </p>
                    </div>
                  </div>
                  <div className="hidden shrink-0 sm:flex sm:flex-col sm:items-end">
                    <div className="flex flex-row">
                      <p className="mt-1 truncate text-xs leading-5 text-gray-500">
                        {`Start: ${convertToCustomFormat(
                          reservation.start_date
                        )}`}
                      </p>
                      <p className="mt-1 truncate text-xs leading-5 text-gray-500 ml-5">
                        {`Finish: ${convertToCustomFormat(
                          reservation.finish_date
                        )}`}
                      </p>
                    </div>
                    <p className="mt-1 truncate text-xs leading-5 text-gray-500">
                      {`Total Price: ${reservation.total_price} TL`}
                    </p>
                    <button
                      type="button"
                      className="mt-4 inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      onClick={() => handleDelete(reservation.reservation_id)}
                    >
                      {loading ? "loading" : "Delete"}
                    </button>
                  </div>
                </li>
              ))}
        </ul>
      </div>
    </>
  );
}
