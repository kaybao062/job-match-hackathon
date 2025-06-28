'use server'

import { createClientForServer } from "@/lib/supabase/server"

type PreferencesParams = {
  sortBy: string;
  employmentType: string;
  maxDaysOld: string;
  salaryRange: [number, number];
  company: string;
};

const updateParameters = async (params:PreferencesParams) => {
    const supabase = await createClientForServer()

    const formFields = {
        sort_by: params.sortBy,
        employment_type: params.employmentType,
        max_days_old: params.maxDaysOld,
        salary_min: params.salaryRange[0],
        salary_max: params.salaryRange[1],
        target_company: params.company,
    };

    const {
        data: { user },
        error: authError,
    } = await supabase.auth.getUser();

    if (authError) {
        console.error("Auth error:", authError);
        throw authError;
    }
    if (!user) {
        console.error("No user found in session");
        throw new Error("No user logged in");
    }

    console.log("Updating preferences for user:", user.id);
    console.log("Form fields to update:", formFields);

    // First, let's check if the user exists
    const { data: userData, error: userError } = await supabase
        .from("users")
        .select("*")
        .eq("id", user.id)
        .single();

    console.log("User check - data:", userData);
    console.log("User check - error:", userError);

    if (userError) {
        console.error("Error checking user:", userError);
        return {
            success: false,
            error: userError.message,
            formFields,
        };
    }

    if (!userData) {
        console.error("User not found in database");
        return {
            success: false,
            error: "User not found in database",
            formFields,
        };
    }

    const { data, error } = await supabase
        .from("users")
        .update(formFields)
        .eq("id", user.id)
        .select();

    console.log("Update response - data:", data);
    console.log("Update response - error:", error);

    if (error) {
        return {
            success: false,
            error: error.message,
            formFields,
        };
    }

    return {
        success: true,
        data,
    };

}

export {updateParameters};