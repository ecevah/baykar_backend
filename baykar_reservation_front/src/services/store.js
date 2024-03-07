"use client";
import { configureStore } from "@reduxjs/toolkit";
import { setupListeners } from "@reduxjs/toolkit/query";
import { usersApi } from "./apis/users_api";

export const store = configureStore({
  reducer: {
    [usersApi.reducerPath]: usersApi.reducer,
  },
  middleware: (getDefaultMiddleware) => {
    return getDefaultMiddleware().concat(usersApi.middleware);
  },
});

setupListeners(store.dispatch);

export {
  useFetchUsersQuery,
  useAddReservationMutation,
  useFetchIHAsQuery,
  useFetchReservationsQuery,
  useLoginMutation,
  useAddUsersMutation,
  useRemoveReservationMutation,
} from "./apis/users_api";
