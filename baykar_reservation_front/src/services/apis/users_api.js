"use client";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

const URL = "http://127.0.0.1:8000/";

const usersApi = createApi({
  reducerPath: "users",
  baseQuery: fetchBaseQuery({
    baseUrl: URL,
  }),
  tagTypes: ["Users"],
  endpoints(builder) {
    return {
      fetchUsers: builder.query({
        providesTags: ["Users"],
        query: () => {
          return {
            url: "/api/customers",
            method: "GET",
            headers: {
              Authorization: localStorage.getItem("token"),
            },
          };
        },
      }),
      addUsers: builder.mutation({
        invalidatesTags: () => {
          return [{ type: "User" }];
        },
        query: (body) => {
          return {
            url: "/api/customer/create",
            method: "POST",
            body,
            headers: {
              Authorization: localStorage.getItem("token"),
            },
          };
        },
      }),
      removeUsers: builder.mutation({
        invalidatesTags: () => {
          return [{ type: "User" }];
        },
        query: (user) => {
          return {
            url: `/api/customer/delete/${user.id}`,
            method: "DELETE",
            headers: {
              Authorization: localStorage.getItem("token"),
            },
            body: {
              name: "Can",
            },
          };
        },
      }),
      login: builder.mutation({
        invalidatesTags: () => {
          return [{ type: "User" }];
        },
        query: (body) => {
          return {
            url: "/login",
            method: "POST",
            body,
          };
        },
      }),
      fetchIHAs: builder.query({
        providesTags: ["Users"],
        query: () => {
          return {
            url: "/api/ihas",
            method: "GET",
            headers: {
              Authorization: localStorage.getItem("token"),
            },
          };
        },
      }),
      fetchReservations: builder.query({
        providesTags: ["Users"],
        query: () => {
          return {
            url: `/api/reservation/find?customer_username=johndoe`,
            method: "GET",
            headers: {
              Authorization: localStorage.getItem("token"),
            },
          };
        },
      }),
      addReservation: builder.mutation({
        invalidatesTags: () => {
          return [{ type: "User" }];
        },
        query: (body) => {
          return {
            url: "/api/reservation/create",
            method: "POST",
            body,
            headers: {
              Authorization: localStorage.getItem("token"),
            },
          };
        },
      }),
      removeReservation: builder.mutation({
        invalidatesTags: ["Users"],
        query: (reservationId) => {
          return {
            url: `/api/reservation/delete/${reservationId}`,
            method: "DELETE",
            headers: {
              Authorization: localStorage.getItem("token"),
            },
          };
        },
      }),
    };
  },
});

export const {
  useFetchUsersQuery,
  useAddUsersMutation,
  useLoginMutation,
  useAddReservationMutation,
  useFetchIHAsQuery,
  useFetchReservationsQuery,
  useRemoveReservationMutation,
} = usersApi;
export { usersApi };
