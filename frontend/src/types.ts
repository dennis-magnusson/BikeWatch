interface Location {
    value: `city:${string}` | `region:${string}`;
    label: string;
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
    size: string;
    description: string;
    short_description: string | null;
    date_posted: string;
    date_last_updated: string;
    date_first_seen: string;
    images: Image[];
}

export type { Image, Listing, Location };
