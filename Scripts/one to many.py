import arcpy

# 1. Set environment workspace to your file geodatabase
arcpy.env.workspace = r"C:\Users\mtcuster\Documents\ArcGIS\Projects\Local empowerment\Local_empowement_processeddata08192026.gdb"
arcpy.env.overwriteOutput = True

# 2. Define input features and tables (Must be inside the same .gdb)
target_layer = r"pa"
join_table = "CAIs_Eligible_for_BOTB"

# Fields used to link the layers
target_key = "GRID_ID"
join_key = "Application_Area"

# 3. Create a temporary Feature Layer from the geodatabase feature class
# (AddJoin requires a layer object or layer name, not a direct path)
lyr_name = "hexbins"
arcpy.management.MakeFeatureLayer(target_layer, lyr_name)

# 4. Execute the AddJoin tool with the "KEEP_ALL" and "JOIN_ONE_TO_MANY" options
print("Executing one-to-many join...")
arcpy.management.AddJoin(
    in_layer_or_view=lyr_name,
    in_field=target_key,
    join_table=join_table,
    join_field=join_key,
    join_type="KEEP_ALL",
    join_operation="JOIN_ONE_TO_MANY"  # Forces true 1:M duplication
)

# 5. Export features to make the duplicated geometry permanent
output_features = "CAIs_Eligible_for_BOTB_hexbins"
print(f"Exporting results to permanent feature class: {output_features}...")
arcpy.management.CopyFeatures(lyr_name, output_features)

print("One-to-many join successfully completed!")

print("selecting empty hexbins...")
selection = arcpy.management.SelectLayerByAttribute(output_features, "NEW_SELECTION", "CAIs_Eligible_for_BOTB_location_id IS NULL")
print(int(arcpy.management.GetCount(selection)[0]))
if int(arcpy.management.GetCount(selection)[0]) > 0:
    print("Found empty hexbins. Deleting...")
    arcpy.management.DeleteFeatures(selection)