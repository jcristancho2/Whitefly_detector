// Archivo: android/build.gradle.kts

plugins {
    id("com.android.application") version "8.7.3" apply false
    id("com.android.library") version "8.7.3" apply false
    id("org.jetbrains.kotlin.android") version "2.1.0" apply false
}

// Directorio de compilación raíz
rootProject.buildDir = file("../build")

// Configuración de subproyectos
subprojects {
    project.buildDir = file("${rootProject.buildDir}/${project.name}")
    project.evaluationDependsOn(":app")
}

// Tarea "clean"
tasks.register<Delete>("clean") {
    delete(rootProject.buildDir)
}
