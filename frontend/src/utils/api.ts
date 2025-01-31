import axios from "axios";
import { Listing, Location } from "../types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

interface FetchListingsResponse {
    total: number;
    listings: Listing[];
}

export const fetchListings = async (
    params: string
): Promise<FetchListingsResponse> => {
    try {
        const url = `${BASE_URL}/listings?${params}`;
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error("Error fetching listings: ", error);
        return { total: 0, listings: [] };
    }
};

export const fetchLocations = async (): Promise<Location[]> => {
    try {
        const url = `${BASE_URL}/locations`;
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error("Error fetching locations: ", error);
        return [];
    }
};

interface Filters {
    sortBy: string;
    maxPrice: number;
    minPrice: number;
    locationFilters: Location[];
    size: number;
    showAllSizes: boolean;
    sizeFlexibility: boolean;
    selectedCategories: string[];
    page: number;
}

export const formatUrlParams = (filters: Filters): string => {
    const params = new URLSearchParams();

    if (filters.sortBy) {
        params.append("sort_by", filters.sortBy);
    }

    if (filters.maxPrice !== Infinity) {
        params.append("max_price", filters.maxPrice.toString());
    }

    if (filters.minPrice) {
        params.append("min_price", filters.minPrice.toString());
    }

    if (filters.locationFilters.length > 0) {
        filters.locationFilters.forEach((loc: Location) => {
            if (loc.locationType === "city") {
                params.append("city", loc.name);
            } else {
                params.append("region", loc.name);
            }
        });
    }

    if (!filters.showAllSizes) {
        params.append("size", filters.size.toString());
        if (filters.sizeFlexibility) {
            params.append("size_flexibility", "true");
        }
    }

    if (filters.selectedCategories.length > 0) {
        filters.selectedCategories.forEach((category: string) => {
            params.append("category", category);
        });
    }

    params.append("pagination", filters.page.toString());

    return params.toString();
};
