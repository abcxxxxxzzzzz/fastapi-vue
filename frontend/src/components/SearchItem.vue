<template>
    <el-col :span="6" :offset="0">
        <el-form-item :label="label">
            <slot />
        </el-form-item>
    </el-col>
</template>


<script setup>

defineProps({
    label: String
})

</script>