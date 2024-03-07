import { useRouter } from "next/navigation";

export default function useVerify() {
  const router = useRouter();
  const URL = "http://localhost:8000/";

  const verify = async () => {
    try {
      const token = localStorage.getItem("token");
      if (token) {
        const response = await fetch(`${URL}api/verify`, {
          headers: {
            Authorization: token,
          },
        });

        if (response.ok) {
          const data = await response.json();
          if (data.status === true) {
            return true;
          } else {
            router.push("/");
            return false;
          }
        } else {
          throw new Error("Network response was not ok.");
        }
      } else {
        router.push("/");
        return false;
      }
    } catch (error) {
      console.error(error);
      return false;
    }
  };

  return { verify };
}
