import SwiftUI

struct ContentView: View {
    @StateObject private var catalog = CatalogStore()

    var body: some View {
        NavigationStack {
            List {
                Section { TextField("Buscar", text: $catalog.query) }
                Section("Resultados") {
                    ForEach(catalog.filtered) { item in
                        VStack(alignment: .leading, spacing: 4) {
                            Text(item.name).font(.headline)
                            Text("Atualizado em \(item.lastVerified)").font(.caption).foregroundStyle(.secondary)
                        }
                    }
                }
            }
            .navigationTitle("Example App")
            .overlay {
                if catalog.items.isEmpty { ContentUnavailableView("Catálogo vazio", systemImage: "square.grid.2x2") }
            }
        }
    }
}

#Preview { ContentView() }
