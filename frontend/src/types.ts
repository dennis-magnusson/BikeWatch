interface Location {
    locationType: "city" | "region";
    name: string;
}

interface Image {
    bike_id: string;
    image_url: string;
    id: number;
}

interface Listing {
    id: string;
    title: string;
    url: string;
    brand: string;
    model: string;
    year: number | null;
    price: number;
    region: string;
    city: string;
    number_size_min: string | null;
    number_size_max: string | null;
    letter_size_min: string | null;
    letter_size_max: string | null;
    description: string;
    date_posted: string;
    date_last_updated: string;
    date_first_seen: string;
    images: Image[];
}

type SortBy = "newest" | "oldest" | "price_dec" | "price_inc";

export type { Image, Listing, Location, SortBy };
